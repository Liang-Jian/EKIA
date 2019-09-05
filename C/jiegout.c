#include <stdio.h>
int main(){
    struct name //生命结构提变量,
    {
        int num;
        char ch[20];
        float fnum;
    };
    struct name p;
    typedef struct name num; //typedef给结构体变量取别名
    return 0;
}

#define PRAISE "what a super marvelous name! "

int parise2(){
	char name[40];
	printf("Whats you name \n");
	scanf("%s",name);
	printf("Hello,%s . %s \n", name,PRAISE);
	printf("Your name of %d letters occupies %d memory cells\n", strlen(name),sizeof name);
	printf("and occupies %d memory cells.\n", sizeof PRAISE);
	return 0;
}