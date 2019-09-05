#include <stdio.h>

#define PAGES 334
#define WORDS 65618



int floatcm(){
	float n1 = 3.0;
	double n2 = 3.0;
	long n3 = 20000000;
	long n4 = 1234567890;

	printf("%.1e %.1e %.1e \n", n1,n2,n3,n4);
	printf("%ld %ld \n", n3,n4);
	printf("%ld %ld %ld %ld \n", n1,n2,n3,n4);

	return 0;
}

int main(void){
	short num = PAGES;
	short mnum = -PAGES;

	printf("num as short and unsigned short: %hd %hu \n", num,num);
	printf("-num as short and unsigned short: %hd %hu \n", mnum,mnum);
	printf("num as int and char: %d %c \n", num,num);
	printf("WORDS as int ,short ,and char: %d  %hd %c \n", WORDS,WORDS,WORDS);
	return 0;
}