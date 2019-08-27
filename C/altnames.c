#include <stdio.h>
#include <inttypes.h>

int main (void){
	int16_t = mel6;
	mel6 =4594;
	printf("First,asssume itn16_t is short\n:", );
	printf("mel6 = %hd \n", mel6);
	printf("Next,let's not make any assumptions \n", );
	printf("Instead,use a \"macro\" from inttypes.h \n", );
	printf("mel6 = %" PRID16 "\n", mel6);
	return 0;
}