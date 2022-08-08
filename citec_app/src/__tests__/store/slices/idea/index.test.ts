// Copyright (C) 2021-Present CITEC Inc. <https://citecsolutions.com/>
// All rights reserved
//
// This file is part of CITEC Inc. source code.
// This software framework contains the confidential and proprietary information
// of CITEC Inc., its affiliates, and its licensors. Your use of these
// materials is governed by the terms of the Agreement between your organisation
// and CITEC Inc., and any unauthorised use is forbidden. Except as otherwise
// stated in the Agreement, this software framework is for your internal use
// only and may only be shared outside your organisation with the prior written
// permission of CITEC Inc.
// CITEC Inc. source code can not be copied and/or distributed without the express
// permission of CITEC Inc.
import reducer, { removeIdea, resetIdeas } from 'store/slices/ideas'

const initialState = [] as any

describe('Ideas tests', () => {

   test('Reset Ideas', () => {
      const intermediateState =
      {
         portfolio_id: 16,
         portfolio: 'my_first_portfolio_sadasd',
         benchmark: 'SPY',
         creation_date: '2022-04-06 16:10:19',
         ticker: [
            'MSFT',
            'AAPL'
         ],
         outstanding_balance: [
            200000,
            100000
         ],
         unrealized_capital_gains: [
            0,
            35700
         ],
         optimization_status: null
      }

      expect(reducer(intermediateState as any, resetIdeas())).toEqual(
         initialState
      )
   })

   test('Testing RemoveIdea reducer', () => {
      const intermediateState =[
         {
            portfolio_id: 16,
            portfolio: 'my_first_portfolio_sadasd',
            benchmark: 'SPY',
            creation_date: '2022-04-06 16:10:19',
            ticker: [
               'MSFT',
               'AAPL'
            ],
            outstanding_balance: [
               200000,
               100000
            ],
            unrealized_capital_gains: [
               0,
               35700
            ],
            optimization_status: null
         },
         {
            portfolio_id: 17,
            portfolio: 'Portfolio 2',
            benchmark: 'SPY',
            creation_date: '2022-04-06 16:10:19',
            ticker: [
               'MSFT',
               'AAPL'
            ],
            outstanding_balance: [
               200000,
               100000
            ],
            unrealized_capital_gains: [
               0,
               35700
            ],
            optimization_status: null
         }
      ]

      const resp = [{
         portfolio_id: 16,
         portfolio: 'my_first_portfolio_sadasd',
         benchmark: 'SPY',
         creation_date: '2022-04-06 16:10:19',
         ticker: [
            'MSFT',
            'AAPL'
         ],
         outstanding_balance: [
            200000,
            100000
         ],
         unrealized_capital_gains: [
            0,
            35700
         ],
         optimization_status: null
      }]
      

      expect(reducer(intermediateState as any, removeIdea(17))).toEqual(resp)
   })

})
