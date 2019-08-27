//
// Created by itw_shict on 2018/11/22.达内教程

//

#include <stdio.h>
#include <string.h>
/*

const int ci = 100;

int main(){
    char* str = "abcdef";
//    str[0] = 'A';//段错误，
    strcpy(str,"ABCDEF"); //段错误，
    int* pi = (int*)&ci;//段错误，
}
*/

int main() {
    int x = 10;//fenpei 4bytesde space
    x = "abc";
    printf("x=%s\n",x);
    strcpy(&x,"abc");
    printf("&x=%s\n",&x);

    if (x){
        int ix = 100;
        printf("ix=%d \n",ix);
    }
    ix++; //已经释放，不能访问。
}
