#include <stdio.h>

int main(void){
	printf("Type int has a size of %u bytes.\n", siezeof(int));
	printf("Type char has a size of %u bytes.\n", siezeof(char));
	printf("Type long has a size of %u bytes.\n", siezeof(long));
	printf("Type double has a size of %u bytes.\n", siezeof(double));
	
	return 0;

}