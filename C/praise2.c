#include <stdio.h>
#include <string.h>
#define PRAISE "what a super marvelous name! "

int main(void){
	char name[40];
	printf("Whats you name \n");
	scanf("%s",name);
	printf("Hello,%s . %s \n", name,PRAISE);
	printf("Your name of %d letters occupies %d memory cells\n", strlen(name),sizeof name);
	printf("and occupies %d memory cells.\n", sizeof PRAISE);
	return 0;
}