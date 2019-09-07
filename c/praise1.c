#include <stdio.h>
#define PRAISE "what a super marvelous name!"
//使用字符串

int main(void){
	char name[40];
	printf("what's you name?\n");
	scanf("%s",name);
	printf("Hello. %s .%s \n", name,PRAISE);
	return 0;

}