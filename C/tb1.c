#include <stdio.h>

int main()
{
	float a = 12.5;
	double b = 16.23;
	double c = 0.12312435435465464;
	printf("%g",a);
	printf("%f.5\n",c);
	char d = 'c';
	printf("c is %d\n",d);

	short a1=0;
	printf("%d",sizeof(a1));
	printf("%d",sizeof(short));

	int s1 = 0 , s2 = 0;
	printf("enerter sanjiaoxing");
	scanf("%d %d",&s1,&s2);
	int nu = s1 * s2 /2;
	printf("%d",nu);

	const int b1 =100;
	printf("%d",b1);
	int cc = 10;
	cc =++cc; 
        printf("%d",cc);
	int k = 85;
	printf("%c",k);

	char ch = 'a';
	printf("%hhd",ch);
	
	printf("%010d ,%010d ",123,456);	

	return 0;
}
