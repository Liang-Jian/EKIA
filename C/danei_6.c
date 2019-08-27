//
// Created by itw_shict on 2018/11/22.
//

#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>



struct Emp{
    char name[10];
    int age;
    double salary;
};

int main(){
//    mmap(NULL,50,PROT_READ|PROT_WRITE,);
    int fd = open("emp.dat",0_WRONLY|0_CREAT|0_TRUNC,0666);
    if (fd == -1) perror("create file filed"),exit(-1);
    printf("create file success \n");
    struct Emp e = {"Danile",30,1234356.45};
    ssize_t res = write(fd,&e,sizeof(e));
    if(res <=0){
        perror("write failed)");
        return -1;
    }
    printf("wrete success %d byte\n",res);
    close(fd);


}
