//*****************************************************************************
//
// blinky.c - Simple example to blink the on-board LED.
//
// Copyright (c) 2013-2020 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.2.0.295 of the EK-TM4C1294XL Firmware Package.
//
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
//#include "driverlib/debug.h"
#include "inc/hw_ints.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"

//*****************************************************************************
//
//! \addtogroup example_list
//! <h1>Blinky (blinky)</h1>
//!
//! A very simple example that blinks the on-board LED using direct register
//! access.
//
//*****************************************************************************

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif

//*****************************************************************************
//
// Blink the on-board LED.
//
//*****************************************************************************
uint32_t FS = 120000000*2;
void timer0A_handler(void);
uint8_t switch_state = 0;
uint32_t button = 0;

int main(void)
{
    //Clock Configuration
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000);
    //Enable Peripherals
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    //Enable Timer Peripheral
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    //
    // Check if the peripheral access is enabled.
    //
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION))
    {
    }
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {
    }
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    {
    }
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_TIMER0))
    {
    }

    //
    // Enable the GPIO pin for the LED (PN0).  Set the direction as output, and
    // enable the GPIO pin for digital function.
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, 0x00);
    //Configures input current strenght and pull type
    GPIOPadConfigSet(GPIO_PORTJ_BASE,GPIO_PIN_0|GPIO_PIN_1,GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    
    //Set timer
    TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
    //Set the cout time for Timer
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    //Enable processor interrupts
    IntMasterEnable();
    //Enable Interrupt
    IntEnable(INT_TIMER0A);
    //Enable timer A interrupt
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    //Enable the timer
    TimerEnable(TIMER0_BASE,TIMER_A);
    
    //
    // Loop forever.
    //
    while(1)
    {
      //vacio
    }
}

void timer0A_handler(void)
{
  switch_state++;
  //Changing the timer delay
  if (GPIOPinRead(GPIO_PORTJ_BASE, 0x00) == 0)
  {
    button++;
  }
  if(button>0)
  {
    FS=120000000*4;
    TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
  }
  //Clear timer
  TimerIntClear(TIMER0_BASE, TIMER_A);
  //Sequence 1.
  if(switch_state % 2 != 0)
  {
    GPIOPinWrite(GPIO_PORTN_BASE,0x03,0x02);
    GPIOPinWrite(GPIO_PORTN_BASE,0x11,0x01);
  }
  //Sequence 2.
  if(switch_state % 2 == 0)
  {
    GPIOPinWrite(GPIO_PORTN_BASE,0x03,0x01);
  }
}
