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
from importlib.resources import path
from pathlib import Path
from typing import Iterable, List, Union
import click

LICENSE_HEADER = (
    Path(__file__).parent.joinpath("license_header.txt").read_text().strip()
)
FOLDER_FRONT = "citec_app"


def files_at_path(path: Union[Path, str]) -> List[Path]:

    files_result = []
    extensions = ("py",)
    if FOLDER_FRONT in path:
        extensions = ("ts", "tsx")

    if isinstance(path, str):
        path = Path(path)
    if path.is_dir():
        for extension in extensions:
            files_result.extend(path.rglob("*." + extension))
        return files_result
    return [path]


def files_missing_substring(files: List[Path], substring: str) -> Iterable[Path]:
    for file_ in files:
        with file_.open("r", encoding="utf-8") as current_file:
            content = current_file.read()

        if content.strip() and substring not in content:
            yield file_


@click.command()
@click.option(
    "--exclude",
    "-e",
    help="File or folder to exclude",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
    multiple=True,
)
@click.argument(
    "targets",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
)
def cli(exclude, targets):
    """Checks for legal compliance."""
    if not targets:
        raise click.UsageError("Please provide one or more targets.")

    exit_code = 0

    # find all .py files recursively
    files = []
    for target in targets:
        files.extend(files_at_path(target))

    # glob excluded files
    to_exclude = []
    for ex in exclude:
        to_exclude.extend(files_at_path(ex))
    files = [f for f in files if f not in to_exclude]

    click.secho("\nChecking License in {} files...".format(len(files)), nl=False)

    # find all files which do not contain the header and are non-empty
    if FOLDER_FRONT in target:
        missing_license_files = list(
            files_missing_substring(files, LICENSE_HEADER.replace("#", "//"))
        )
    else:
        missing_license_files = list(files_missing_substring(files, LICENSE_HEADER))

    # exit with an error and print all files without header in read, if any
    if missing_license_files:
        click.secho(
            "\n\nWARNING!: The license header is missing:\n- "
            + "\n- ".join([str(f) for f in missing_license_files]),
            fg="red",
        )
        if FOLDER_FRONT in target:
            click.secho(
                "\nWARNING!: Add it by copy-pasting the below:\n\n"
                + LICENSE_HEADER.replace("#", "//")
                + "\n"
            )
        else:
            click.secho(
                "\nWARNING!: Add it by copy-pasting the below:\n\n"
                + LICENSE_HEADER
                + "\n"
            )
        exit(1)

    click.secho("✅\n")
    exit(0)


if __name__ == "__main__":
    cli()  # pylint:disable=no-value-for-parameter
