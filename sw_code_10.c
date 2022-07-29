#include <stdio.h>
#include <math.h>
#include "platform.h"
#include "xdft_pipe.h"
#include "xparameters.h"

// from xparameters.h
#define XF_DEVICE_ID  	XPAR_DFT_PIPE_0_DEVICE_ID

XDft_pipe XFT;// Instance for Vivado HLS Generated IP

int main()
{
  int i,Status;
  XDft_pipe_Config *ConfigPtr;

  // Initialization
  init_platform();
  XDft_pipe_Initialize( &XFT,XPAR_DFT_PIPE_0_DEVICE_ID);
  ConfigPtr = XDft_pipe_LookupConfig(XF_DEVICE_ID);
  Status =  XDft_pipe_CfgInitialize(&XFT, ConfigPtr);
  if (Status != XST_SUCCESS) {
    return XST_FAILURE;
  }
  Status = XDft_pipe_IsIdle(&XFT);

  //Generate wave
    float real[16], imag[16];
    float d = 2.0 * M_PI / 16;

    for (int i = 0; i < 16; i++) {
        real[i] = sin(1.0 * i * d); //1Hz Sin Wave
        real[i] += sin(3.0 * i * d + M_PI_4); // 3Hz Sin Wave
        real[i] += sin(5.0 * i * d + M_PI_2); // 5Hz Sin Wave
        imag[i] = 0.0;
    }

  //DFT
    while(!XDft_pipe_IsReady(&XFT)) ;  // Check Ready Signal

    XDft_pipe_Write_real_r_Words(&XFT, 0, real, 16); //Write real part
    XDft_pipe_Write_imag_Words(&XFT, 0, imag, 16); //Write iamg part

    XDft_pipe_Start(&XFT);         // Start HW
    while (!XDft_pipe_IsDone(&XFT)) ;  // Wait Done signal

    XDft_pipe_Read_real_r_Words(&XFT, 0, real, 16); //Read real part
    XDft_pipe_Read_imag_Words(&XFT, 0, imag, 16);    //Read imag part

    //Print

    for (int i = 0; i < 16; i++) {
        printf("%dHz %f\n", i, sqrt(real[i] * real[i] + imag[i] * imag[i]));
    }

}