//
// Created by itw_shict on 2018/11/22.
//

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
    int PSZ = getpagesize();
    printf("page size:%d\n",PSZ);
    int* pi = malloc(4);

    *(pi + 1023) = 100;
    *pi = 123;
    printf("pi=%p\n",pi);
    while (1);
}
