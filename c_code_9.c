#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//#include "ap_int.h"

#define N 11
#define PREC 65536 // 2**16 sign + 15bit precision

/* comment out for bitwith optmization part
typedef ap_int<16> data_t;
typedef ap_int<16> coef_t;
typedef ap_int<24> acc_t;
*/
typedef int data_t;
typedef int coef_t;
typedef int acc_t;


int fir_unroll(int *y, int x)
{
	// Edited part
	static int cycle = 0;
	coef_t c[N] = { // 0.17 = 20KHz/44.1KHz, LPF, Hamming Window
		-136, -397, -87, 3004, 8338, 11142, 8338,
		3004, -87, -397, -136, };

	static data_t shift_reg[N];
	acc_t acc;
	int i;
	acc = 0;
	FIR_LOOP: for (i = N - 1; i >= 0; i--) {
		cycle++;
		if (i == 0) {
			acc += x * c[0];
			shift_reg[0] = x;
		} else {
			shift_reg[i] = shift_reg[i - 1];
			acc += shift_reg[i] * c[i];
		}
	}
	*y = acc;
	return cycle;
}


int main()
{
	int len = 10;
	int fir_out;
	int i;
	for( i = 0; i < len; i++){
		fir_unroll(&fir_out, i);
		printf("result=d%",i);
	}
	return 0;
}