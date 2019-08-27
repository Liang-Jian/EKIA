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