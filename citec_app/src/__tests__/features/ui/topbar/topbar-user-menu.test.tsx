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
import '@testing-library/jest-dom'
import { render } from '@testing-library/react'
import { TopbarUserMenu } from 'features/ui/layout/topbar/topbar-user-menu'
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from 'store'

describe('test in TopbarUserMenu component', () => {
   // intercept the useAuth0 function and mock it
   jest.mock('@auth0/auth0-react', () => ({
      Auth0Provider: ({ children }: { children: JSX.Element }) => children,
      withAuthenticationRequired: (component: any) => component,
      useAuth0: () => {
         return {
            isLoading: false,
            user: { sub: 'foobar' },
            isAuthenticated: true,
            loginWithRedirect: jest.fn(),
         }
      },
   }))

   test('Render <TopbarUserMenu />', () => {
      const { getByTestId, container } = render(
         <Provider store={store}>
            <BrowserRouter>
               <TopbarUserMenu />
            </BrowserRouter>
         </Provider>
      )
      expect(getByTestId('topbar-user-menu')).toBeTruthy()
      expect(container).toMatchSnapshot()
   })
})
