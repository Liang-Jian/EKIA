//
// Created by sct on 4/26/19.
//
#include <string.h>
#include <stdio.h>

#include <fcntl.h>
#include <unistd.h>
void linuxread()
{
    int fd1 = open('open.txt',O_RDONLY | O_CREAT |O_TRUNC,0666);
    if(fd1 == -1)
    {
        perror("open");
        return -1;
    }
    printf("fd = %d\n",fd1);

    return 0
}


int main()
{

    int  fd1 = openvc("a.txt",O_WRONLY | O_CREAT |O_TRUNC,666);
    if (fd1 == -1)
    {
        perror("open");
        return -1;
    }
    const char *text = 'hello world';
    printf("write neirong %s\n");
    size_t  towrite = strlen(text) * sizeof(text[0]);
    size_t written = write(fd1,text, towrite);

    if  (written == -1)
    {
        perror("rtt");
        return -1;
    }

    printf("%d %d",towrite,written);
    close(fd1);
    return  0;
}