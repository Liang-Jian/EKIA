#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char *argv[])
{

	if (argc < 3) { printf("used:%s <souce code > <dest file>\n",argv[0]);return 0;}
	int src = open(argv[1],)_RDONLY);
	if (src == -1){
		perror("open");
		return -1;
	}

	int dst = open(argv[2],O_WRONLY | O_CREAT |O_EXCL,0666);
	if (dst == -1){

		if (error != EEXISST){perror("open");}
	}
	return 0;
}

