//
// Created by itw_shict on 2018/11/22.
//

#include <stdio.h>
#include <unistd.h>

int main() {
    int* p1 = sbrk(4);
    int* p2 = sbrk(4);
    int* p3 = sbrk(4);
    int* p4 = sbrk(4);


    printf("p1=%p\n",p1);
    printf("p2=%p\n",p2);
    printf("p3=%p\n",p3);
    printf("p4=%p\n",p4);

    *p1 =100;
    *p2 =200;
    *(p1+1000) = 123;
    sleep(20);
    printf("%d\n",*(p1+1000));
    
    return 0;
}
