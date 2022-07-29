#include <stdio.h>
#include "platform.h"
#include "xfir_unroll.h"
#include "xparameters.h"

// from xparameters.h
#define XF_DEVICE_ID  	XPAR_FIR_UNROLL_0_DEVICE_ID

XFir_unroll XFT;// Instance for Vivado HLS Generated IP

int main()
{
  int i,Status;
  XFir_unroll_Config *ConfigPtr;
  int in_x;
  int ou_y;
  int cycle;

  // Initialization
  init_platform();
  XFir_unroll_Initialize( &XFT,XPAR_FIR_UNROLL_0_DEVICE_ID);

  ConfigPtr = XFir_unroll_LookupConfig(XF_DEVICE_ID);
  Status =  XFir_unroll_CfgInitialize(&XFT, ConfigPtr);
  if (Status != XST_SUCCESS) {
    return XST_FAILURE;
  }
  Status = XFir_unroll_IsIdle(&XFT);

  for (i=0;i<10;i++) {
    printf("Original coefficients are: -136, -397, -87, 3004, 8338, 11142, 8338,\n
		3004, -87, -397, -136")
    printf("TEST START %d:\n",i);
    in_x=i;
    while(!XFir_unroll_IsReady(&XFT)) ;  // Check Ready Signal
    XFir_unroll_Set_x(&XFT, in_x);  // Set register x
    ou_y = XFir_unroll_Get_y(&XFT);

    XFir_unroll_Start(&XFT);         // Start HW
    while (!XFir_unroll_IsDone(&XFT)) ;  // Wait Done signal

    ou_y = (int)XFir_unroll_Get_y(&XFT); // Load register y
    cycle = XFir_unroll_Get_return(&XFT);

    printf("Get value y = %d(%d)\n", ou_y, i);
  }

  printf("Test done.\n");
  cleanup_platform();
  return 0;
}