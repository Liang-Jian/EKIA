#include <studio.h>

int main(void){
	float salary;
	printf("\a Enter you desired mothly salary: ");
	printf(" $_____\b\b\b\b ");
	scanf("%f",&salary);
	printf("\n\t$ %.2f a month is $%.2f a year",salary,salary * 12.0);
	printf("\rGee\n");
	return 0;

}