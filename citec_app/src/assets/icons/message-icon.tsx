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

interface MessageProps {
   color: 'white' | 'green'
}

export const Message = ({ color }: MessageProps) => {
   let colorIcon

   if (color === 'white') {
      colorIcon = '#79828D'
   } else {
      colorIcon = '#fffff'
   }

   return (
      <svg
         width="22"
         height="23"
         viewBox="0 0 22 23"
         fill="none"
         xmlns="http://www.w3.org/2000/svg"
      >
         <path
            d="M17.4167 22.4993H15.5834C15.3403 22.4993 15.1071 22.4028 14.9352 22.2309C14.7633 22.059 14.6667 21.8258 14.6667 21.5827C14.6667 21.3396 14.7633 21.1064 14.9352 20.9345C15.1071 20.7626 15.3403 20.666 15.5834 20.666H17.4167C18.1461 20.666 18.8456 20.3763 19.3613 19.8606C19.877 19.3448 20.1667 18.6454 20.1667 17.916V16.0827C20.1667 15.8396 20.2633 15.6064 20.4352 15.4345C20.6071 15.2626 20.8403 15.166 21.0834 15.166C21.3265 15.166 21.5597 15.2626 21.7316 15.4345C21.9035 15.6064 22.0001 15.8396 22.0001 16.0827V17.916C21.9986 19.1311 21.5153 20.2961 20.656 21.1553C19.7968 22.0145 18.6319 22.4979 17.4167 22.4993Z"
            fill={colorIcon}
         />
         <path
            d="M0.916666 7.83333C0.673551 7.83333 0.440394 7.73675 0.268485 7.56485C0.0965771 7.39294 0 7.15978 0 6.91666V5.08333C0.00145554 3.8682 0.484808 2.70326 1.34403 1.84403C2.20326 0.984808 3.3682 0.501456 4.58333 0.5L6.41666 0.5C6.65978 0.5 6.89294 0.596577 7.06485 0.768485C7.23675 0.940394 7.33333 1.17355 7.33333 1.41667C7.33333 1.65978 7.23675 1.89294 7.06485 2.06485C6.89294 2.23676 6.65978 2.33333 6.41666 2.33333H4.58333C3.85399 2.33333 3.15451 2.62306 2.63879 3.13879C2.12306 3.65451 1.83333 4.35399 1.83333 5.08333V6.91666C1.83333 7.15978 1.73676 7.39294 1.56485 7.56485C1.39294 7.73675 1.15978 7.83333 0.916666 7.83333Z"
            fill={colorIcon}
         />
         <path
            d="M6.41666 22.4993H4.58333C3.3682 22.4979 2.20326 22.0145 1.34403 21.1553C0.484808 20.2961 0.00145554 19.1311 0 17.916L0 16.0827C0 15.8396 0.0965771 15.6064 0.268485 15.4345C0.440394 15.2626 0.673551 15.166 0.916666 15.166C1.15978 15.166 1.39294 15.2626 1.56485 15.4345C1.73676 15.6064 1.83333 15.8396 1.83333 16.0827V17.916C1.83333 18.6454 2.12306 19.3448 2.63879 19.8606C3.15451 20.3763 3.85399 20.666 4.58333 20.666H6.41666C6.65978 20.666 6.89294 20.7626 7.06485 20.9345C7.23675 21.1064 7.33333 21.3396 7.33333 21.5827C7.33333 21.8258 7.23675 22.059 7.06485 22.2309C6.89294 22.4028 6.65978 22.4993 6.41666 22.4993Z"
            fill={colorIcon}
         />
         <path
            d="M21.0834 7.83333C20.8403 7.83333 20.6071 7.73675 20.4352 7.56485C20.2633 7.39294 20.1667 7.15978 20.1667 6.91666V5.08333C20.1667 4.35399 19.877 3.65451 19.3613 3.13879C18.8456 2.62306 18.1461 2.33333 17.4167 2.33333H15.5834C15.3403 2.33333 15.1071 2.23676 14.9352 2.06485C14.7633 1.89294 14.6667 1.65978 14.6667 1.41667C14.6667 1.17355 14.7633 0.940394 14.9352 0.768485C15.1071 0.596577 15.3403 0.5 15.5834 0.5H17.4167C18.6319 0.501456 19.7968 0.984808 20.656 1.84403C21.5153 2.70326 21.9986 3.8682 22.0001 5.08333V6.91666C22.0001 7.15978 21.9035 7.39294 21.7316 7.56485C21.5597 7.73675 21.3265 7.83333 21.0834 7.83333Z"
            fill={colorIcon}
         />
      </svg>
   )
}