#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.c"

int main(void)
{
    // Configurar la frecuencia del sistema a 120 MHz
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
    
    // Habilitar periféricos
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    
    // Configurar pines PA0 y PA1 para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);
    
    // Configurar pines de salida para motores (PE0, PE1: Motor A; PE2, PE3: Motor B)
    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);
    // Configurar PN1 para buzzer
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    
    // Configurar UART0 a 9600 baudios
    UARTStdioConfig(0, 9600, 120000000);
    
    char rxChar; // Variable para recibir un solo carácter
    
    // Inicializar motores apagados
    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3, 0);
    
    while (1)
    {
        // Recibir datos por UART
        if (UARTCharsAvail(UART0_BASE)) {
            rxChar = UARTCharGet(UART0_BASE); // Leer un carácter
            
            switch (rxChar) {
                case 'F': // Avanzar
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0, GPIO_PIN_0); // IN1=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1, 0);          // IN2=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2, GPIO_PIN_2); // IN3=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_3, 0);          // IN4=0
                    break;
                    
                case 'B': // Retroceder
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0, 0);          // IN1=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1, GPIO_PIN_1); // IN2=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2, 0);          // IN3=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_3, GPIO_PIN_3); // IN4=1
                    break;
                    
                case 'L': // Izquierda
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0, 0);          // IN1=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1, GPIO_PIN_1); // IN2=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2, GPIO_PIN_2); // IN3=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_3, 0);          // IN4=0
                    break;
                    
                case 'R': // Derecha
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0, GPIO_PIN_0); // IN1=1
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1, 0);          // IN2=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2, 0);          // IN3=0
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_3, GPIO_PIN_3); // IN4=1
                    break;
                    
                case 'S': // Detener
                    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3, 0);
                    break;
                    
                case '7': // Activar buzzer brevemente
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
                    SysCtlDelay(12000000); // Retardo
                    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0);
                    break;
            }
        }
    }
