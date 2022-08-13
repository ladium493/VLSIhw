// float samplerate sampling freq.
// float freq  cut-off freq.
// float q    Q value, must q>0, typicall it is set to 1/root(2)
#include <stdio.h>
#include <math.h>

int BFH(float input[16], float output[16], int samplerate, int freq)
{
	int r=0;
	// If the input format is float or double,
	// it cannot be input correctly, and the result will be 'nan'
	// I use int replace float and fix the q to 1/sqrt(2).

	// Set ports
	#pragma HLS INTERFACE s_axilite register port=input bundle=slv0
	#pragma HLS INTERFACE s_axilite register port=output bundle=slv0

	#pragma HLS INTERFACE s_axilite register port=samplerate bundle=slv1
	#pragma HLS INTERFACE s_axilite register port=freq bundle=slv1

	#pragma HLS INTERFACE s_axilite register port=return bundle=slv2

	// filter coefficient
	float omega = 2.0 * M_PI*  freq/samplerate;

	float alpha = sin(omega) / (2.0f * 1/sqrt(2));
 
	float a0 =   1.0f + alpha;
	float a1 =  -2.0f * cos(omega);
	float a2 =   1.0f - alpha;
	float b0 =  (1.0f + cos(omega)) / 2.0f;
	float b1 = -(1.0f + cos(omega));
	float b2 =  (1.0f + cos(omega)) / 2.0f;
 
	// buffers
	float in1  = 0.0f;
	float in2  = 0.0f;
	float out1 = 0.0f;
	float out2 = 0.0f;
 
	// BiQuad Filtering
	for(int i = 0; i < 16; i++)
	{
		output[i] = b0/a0 * input[i] + b1/a0 * in1  + b2/a0 * in2
		                             - a1/a0 * out1 - a2/a0 * out2;

		in2  = in1;
		in1  = input[i];

		out2 = out1;
		out1 = output[i];
		r++;
	}
	return r;
}

int main (int argc, const char * argv[])
{
	//Generate waveform
    float input[16], output[16];

    float d = 2.0 * M_PI / 16;

    for (int i = 0; i < 16; i++) {
    	input[i] = sin(100.0 * i * d); //100Hz Sin Wave
    	input[i] += sin(400.0 * i * d + M_PI_4); // 400Hz Sin Wave
    	input[i] += sin(500.0 * i * d + M_PI_2); // 500Hz Sin Wave
    	output[i] = 0.0f;
    }

    //Apply filter
    BFH(input, output,48000, 400);

    //Get results
    for (int i = 0; i < 16; i++) {
        printf("input=%5.4f, output=%5.4f\n",input[i], output[i]);
    }

    return 0;
}

