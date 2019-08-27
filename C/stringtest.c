#include <stdio.h>
#include <string.h>

int main(){

    // printf("%s\n","abcdefg");
    // printf("%p\n","abcdefg");
    // printf("%c\n",*"abcdefg");
    // // *"abcdef" = "z"; 字符串初春位置不被修改
    // char ch[] = "abc";
    // printf("%d\n",sizeof(ch)); // 4  because add \0 ; so 4 size;

    // char ch[] = "abcdef";
    // printf("%d\n,",strlen(ch)); //strlen only calc fact string length
 
    // char ch[] = "fuck";
    // char buf[30] = "you";
    // printf("合并字符串%s\n",strcat(ch,buf)); //strcat function concat two string 
    // printf("合并字符串,返回新的字符串%s\n",strcpy(buf,"suckmydick,mygirl")); 
    // printf("合并制定后的字符串%s\n",strncpy(buf,"suckmydick,mygirl",4)); 
    // printf("比较两个字符串大小%d\n",strcmp("polytnw","sdifckdfi"));//-1为前面的小 1 后面的小 0 一样
    // printf("%d\n",strncmp("polytnw","sdifckdfi",2));
    // char buf[20] = {};
    // printf("enter string");
    // scanf("%s",buf);
    // printf("%s",buf);  //标准输入文件stdin  标准输出文件stdout

    // char buf[20]={};
    // printf("enter string");
    // fgets(buf,10,stdin);//fgets get string from anyfile , put array in;
    // printf("input string is %s\n",buf);



    // char fuck[5][4] = {"100","200","300","400","500"};
    char *fuck[5] = {"100","200","300","500","324"};
    int num = 0;
    for( num = 0; num <= 4; num++)
    {
        printf("%s\n",fuck[num]);   
        /* code */
    }
    
    return 0;

}