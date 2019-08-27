#include <stdio.h>
int main(){
    struct name //生命结构提变量,
    {
        int num;
        char ch[20];
        float fnum;
    };
    struct name p;
    typedef struct name num; //typedef给结构体变量取别名
    return 0;
}
