#include <stdio.h>
/*
//zhu hanshu args show
int main(int argc,char *argv[]){ // main wirte method only this 
    int num = 0;
    for( num = 0; num <= argc-1; num++)
    {
        printf("%s\n",argv[num]);
    }
    
    return 0;
}*/


//seek_set 文件头当作基准位置
//seek_cur 文件当前当作基准位置
//seek_end 文件尾当作基准位置

int main() {
    FILE *ffile = fopen("abc.txt","rb");
    if (ffile) {
        fseek(ffile,3,SEEK_END);
        printf("位置指针%ld",ftell(ffile)); //ftell get point number
        rewind(ffile,)
        fclose(ffile);
        ffile = NULL;
    }
    return 0;
}