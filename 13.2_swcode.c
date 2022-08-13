/******************************************************************************
*
* Copyright (C) 2009 - 2014 Xilinx, Inc.  All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* Use of the Software is limited solely to applications:
* (a) running on a Xilinx device, or
* (b) that interact with a Xilinx device through a bus or interconnect.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* XILINX  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
* OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
* Except as contained in this notice, the name of the Xilinx shall not be used
* in advertising or otherwise to promote the sale, use or other dealings in
* this Software without prior written authorization from Xilinx.
*
******************************************************************************/

/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */
#include <stdio.h>
#include <math.h>
#include "platform.h"
//#include "xil_printf.h"
#include "xbfh.h"
#include "xparameters.h"

// from xparameters.h
#define XF_DEVICE_ID  	XPAR_BFH_0_DEVICE_ID
// Instance for Vivado HLS Generated IP
XBfh XBQ;

int main()
{
    // Specify parameters
    int samplerate=48000;
    int freq=400;

    // Generate waveform
    float input[16], output[16];

    float d = 2.0 * M_PI / 16;

    for (int i = 0; i < 16; i++) {
    	input[i] = sin(100.0 * i * d); //100Hz Sin Wave
    	input[i] += sin(400.0 * i * d + M_PI_4); // 300Hz Sin Wave
    	input[i] += sin(500.0 * i * d + M_PI_2); // 500Hz Sin Wave
    	output[i] = 0.0f;

    }

    // Initialization
    int Status;
    XBfh_Config *ConfigPtr;
    init_platform();
    XBfh_Initialize( &XBQ,XPAR_BFH_0_DEVICE_ID);
    ConfigPtr = XBfh_LookupConfig(XF_DEVICE_ID);
    Status =  XBfh_CfgInitialize(&XBQ, ConfigPtr);
    if (Status != XST_SUCCESS) {
    return XST_FAILURE;
    }
    Status = XBfh_IsIdle(&XBQ);

    // Apply filter
    while(!XBfh_IsReady(&XBQ)) ;  // Check Ready Signal

    // Write
    XBfh_Set_samplerate(&XBQ, samplerate);
    XBfh_Set_freq(&XBQ, freq);

    XBfh_Write_input_r_Words(&XBQ, 0, input, 16);
    XBfh_Write_output_r_Words(&XBQ, 0, output, 16);

    while(!XBfh_IsReady(&XBQ)) ;  // Check Ready Signal
    XBfh_Start(&XBQ);         // Start HW
    while (!XBfh_IsDone(&XBQ)) ;  // Wait Done signal

    XBfh_Read_output_r_Words(&XBQ, 0, output, 16);  //Read output
    XBfh_Read_input_r_Words(&XBQ, 0, input, 16);

    // Print results
    for (int i = 0; i < 16; i++) {
        printf("input=%5.4f, output=%5.4f\n",input[i], output[i]);

    }
    cleanup_platform();
    return 0;
}
