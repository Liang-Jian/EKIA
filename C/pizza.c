#include <stdio.h>

#define Pi 3.14159 //常量
int main(void){
	float area,circum,radius;
	scanf("%f",&radius);
	area = Pi * radius * radius;
	circum =2.0 * Pi *radius;
	printf("Your base pizza parameters are as follows:\n");
	printf("circumeferece = %1.2f, area=%1.2f \n", circum,area);
	return 0;

}

int typesixze(){
	printf("Type int has a size of %u bytes.\n", siezeof(int));
	printf("Type char has a size of %u bytes.\n", siezeof(char));
	printf("Type long has a size of %u bytes.\n", siezeof(long));
	printf("Type double has a size of %u bytes.\n", siezeof(double));

	return 0;

}


int longstr(){
	printf("Here's one way to print a \n");
	printf("Long string .\n");
	printf("Here's another way to print a long string \n");
	printf("Here's the newest way to print a ** long string .\n");
	return 0;
}