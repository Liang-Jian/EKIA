//
// Created by itw_shict on 2018/11/22.
//

#include <stdio.h>
#include <stdlib.h>

int main(){
    int* p1 = malloc(4);
    int* p2 = malloc(4);
    int* p3 = malloc(4);
    int* p4 = malloc(4);

    printf("p1=%p \n",p1);
    printf("p2=%p \n",p2);
    printf("p3=%p \n",p3);
    printf("p4=%p \n",p4);

    free(p1);
}
