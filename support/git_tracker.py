#!/usr/bin/env python3
# Copyright (C) 2021-Present CITEC Inc. <https://citecsolutions.com/>
# All rights reserved
#
# This file is part of CITEC Inc. source code.
# This software framework contains the confidential and proprietary information
# of CITEC Inc., its affiliates, and its licensors. Your use of these
# materials is governed by the terms of the Agreement between your organisation
# and CITEC Inc., and any unauthorised use is forbidden. Except as otherwise
# stated in the Agreement, this software framework is for your internal use
# only and may only be shared outside your organisation with the prior written
# permission of CITEC Inc.
# CITEC Inc. source code can not be copied and/or distributed without the express
# permission of CITEC Inc.
from typing import Dict, List
import sys
import tempfile
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from subprocess import PIPE, Popen


def _cmd(command):
    return Popen(
        args=command,
        stdout=PIPE,
        shell=True
    ).communicate()[0]


def _load_data(git_email: str = None, after: str = None) -> pd.DataFrame:
    tmp_folder = tempfile.mkdtemp()
    raw_file = os.path.join(tmp_folder, 'data.txt')
    command = 'git rev-list --all --remotes --no-merges'
    if git_email is not None:
        command += ' --author="' + git_email + '"'
    if after is not None:
        command += ' --after=' + after

    command += ' --date=iso --pretty=format:"%C(yellow)%h%Creset'
    command += ' | %ad | %Cgreen%s%Creset %Cred%d%Creset %Cblue | %aE"'
    command += ' > ' + raw_file
    os.system(command)
    return pd.read_csv(
        filepath_or_buffer=raw_file, sep="|",
        names=["commit_hash", "commit_timestamp", "description", "author"],
        header=None
    ).query("commit_timestamp == commit_timestamp")

def _commit_stats(commit: str) -> Dict:
    stats = {
        "files_change": 0,
        "insertions": 0,
        "deletions": 0
    }
    actions = _cmd(
        'git show {}  --stat'.format(commit)
    ).splitlines()[-1].decode().split(",")
    for action in actions:
        if 'file changed' in action:
            stats['files_change'] = int(action.split('file changed')[0])
        if 'insertion(+)' in action:
            stats['insertions'] = int(action.split('insertion(+)')[0])
        if 'deletions(-)' in action:
            stats['deletions'] = int(action.split('deletions(-)')[0])
    return stats

def _fe_data(df: pd.DataFrame) -> pd.DataFrame:
    df["commit_timestamp"] = pd.to_datetime(
        df["commit_timestamp"].apply(lambda x: str(x)[:-6]))
    df.sort_values("commit_timestamp", ascending=True, inplace=True)
    df["prev_commit_timestamp"] = df["commit_timestamp"].shift(1)
    df["date"] = df['commit_timestamp'].dt.date
    df["day"] = df['commit_timestamp'].dt.month
    df["month"] = df['commit_timestamp'].dt.month
    df["year"] = df['commit_timestamp'].dt.year
    df["yearmonth"] = df["year"] * 100 + df["month"]
    df["diff_previous_commit"] = (
            df["commit_timestamp"] - df["commit_timestamp"].shift(1))
    df["diff_previous_commit_hours"] = df.diff_previous_commit.apply(
        lambda x: x.total_seconds()) / 3600

    df.loc[df["date"] != df["date"].shift(1), "prev_commit_timestamp"] = None
    df.loc[df["date"] != df["date"].shift(1), "diff_previous_commit"] = None
    df.loc[df["date"] != df["date"].shift(1), "diff_previous_commit_hours"] = 0

    df = df.merge(
        right=_bulk_commit_stats(df["commit_hash"].tolist())
        , how="left", on="commit_hash")
    df["files_change"].fillna(value=0, inplace=True)
    df["insertions"].fillna(value=0, inplace=True)
    df["deletions"].fillna(value=0, inplace=True)
    return df

def _ts_daily_report(df: pd.DataFrame) -> pd.DataFrame:
    df["num_commits"] = 1
    df["first_commit_date"] = df["commit_timestamp"]
    df["last_commit_date"] = df["commit_timestamp"]
    df["avg_diff_previous_commit_hours"] = df["diff_previous_commit_hours"]
    df["max_diff_previous_commit_hours"] = df["diff_previous_commit_hours"]


    report = df[
        df["description"].apply(
            lambda x:
                "Merge " not in str(x)
        )
    ].groupby(["date", "author"]).agg(
        {
            "num_commits": "sum",
            "first_commit_date": "min",
            "last_commit_date": "max",
            "avg_diff_previous_commit_hours": "mean",
            "max_diff_previous_commit_hours": "max",
            "files_change": "mean",
            "insertions": "mean",
            "deletions": "mean",
        }
    )
    report = report.merge(
        right=df[["author", "date", "first_commit_date", "commit_hash"]].rename(
            columns={"commit_hash": "first_commit_hash"}
        ),
        how="inner",
        on=["author", "date", "first_commit_date"]
    )
    report = report.merge(
        right=df[["author", "date", "last_commit_date", "commit_hash"]].rename(
            columns={"commit_hash": "last_commit_hash"}),
        how="inner",
        on=["author", "date", "last_commit_date"]
    )
    report = report.merge(
        right=df[
            [
                "author", "date", "max_diff_previous_commit_hours",
                "prev_commit_timestamp", "commit_timestamp"
            ]
        ].rename(
            columns={
                "prev_commit_timestamp": "start_diff_commit",
                "commit_timestamp": "end_diff_commit"
            }
        ),
        how="inner",
        on=["author", "date", "max_diff_previous_commit_hours"]
    )
    report["first_commit_hour"] = report["first_commit_date"].dt.hour
    report["last_commit_hour"] = report["last_commit_date"].dt.hour

    report["low_performance"] = 1 * (
            (report["last_commit_hour"] < 18) & (report["first_commit_hour"] >= 9)
    )

    report["low_performance"] += 1 * (
            (report["last_commit_hour"] < 17) & (report["first_commit_hour"] >= 8)
    )

    report["low_performance"] += 1 * (
            (report["max_diff_previous_commit_hours"] >= 5)
            & (report["start_diff_commit"].dt.hour >= 6)
    )

    report["low_performance"] += 1 * (
        (report["num_commits"] <= 2)
    )

    report["low_performance"] = 1 * (report["low_performance"] > 0)

    return report[
        [
            "author", "date", "first_commit_date", "last_commit_date",
            "start_diff_commit", "end_diff_commit", "max_diff_previous_commit_hours",
            "num_commits", "last_commit_hour",
            "files_change", "insertions", "deletions",
            "low_performance"
        ]
    ]

def _bulk_commit_stats(commits_hash: List[str]) -> pd.DataFrame:
    data=[]
    for commit in commits_hash:
        stats = _commit_stats(commit)
        data.append(
            [
                commit, stats["files_change"], stats["insertions"], stats["deletions"]
            ]
        )
    return pd.DataFrame(
        data=data,
        columns=["commit_hash", "files_change", "insertions", "deletions"]
    )

def _main():
    now = datetime.now()
    after = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")

    email="all_users"
    if len(sys.argv)<=1:
        raw_df = _load_data(after=after)
    elif not "@" in email:
        raw_df = _load_data(after=after)
    else:
        email = sys.argv[1]
        raw_df = _load_data(git_email = email, after=after)
    master_df = _fe_data(raw_df.copy())
    daily_report = _ts_daily_report(master_df.copy())

    output_dir = Path('.gitstatistics/' + email)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df.to_excel(
        excel_writer=output_dir / "git_transactions.xlsx", index=False
    )
    master_df.to_excel(
        excel_writer=output_dir / "master_table.xlsx", index=False
    )
    daily_report.to_excel(
        excel_writer=output_dir / "ts_daily_report.xlsx", index=False
    )

    if email == "all_users":
        summary = daily_report[
            daily_report["date"]
            >= pd.to_datetime(datetime.now() - timedelta(days=5)).date()
        ].merge(
            right=daily_report.groupby("author")["date"].max().reset_index(),
            how="inner",
            on=["author", "date"]
        )
        summary.to_excel(
            excel_writer=output_dir / "latest_day_summary_report.xlsx", index=False
        )

if __name__ == "__main__":
    _main()



