#include <stdio.h>
#include <limits.h>
#include <float.h>

/*const int MONTHS = 12;
#define INT_MAX;
#define INT_MIN;*/


int defines(){
	printf("Some umber limits for this system\n");
	printf("Biggest int ; %d \n", INT_MAX);
	printf("Smallest unsigned long ;%lld\n", LLONG_MIN);
	printf("One byte = %d bits on this system.\n", CHAR_BIT);
	printf("Largest double: %e \n", DBL_MAX);
	printf("float precision= %d digits \n", FLT_DIG);
	printf("float epsilon = %e\n", FLT_EPSILON);
	return 0;
}