//
// Created by itw_shict on 2018/11/26.
//
/*

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
int main(){
    int fd = open("a.txt",0_WRONLY|0_CREAT|0_TRUNC,0666);
    if (fd == -1) perror("create failed"),exit(-1);
    int i;
    for (int j = 0; j < 100000 ; ++j) {
        write(fd,&i,4);
    }
    close(fd);


}*/



#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

int main(){
    int fd = open("a.txt",O_RDWR);
    if (fd == -1)perror("open filed"),exit(-1);
    char c;
    read(fd,&c,1);
    printf("c=%c\n",c);
    write(fd,"1",1);
    write(fd,"2",1);
    lseek(fd,4,SEEK_SET);
    write(fd,"3",1);
    lseek(fd,2,SEEK_CUR);

    return 0;
}

