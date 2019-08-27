#include <stdio.h>
//联合类型
int main() {
    typedef union lianhe
    {
        char ch[2];
        int num;
    }lianhe;
    
    lianhe lianhe1;
    lianhe1.num =0 ;
    lianhe1.ch[0] = 'a';
    lianhe1.ch[1] = 'b';
    printf("%x",lianhe1.num);
    return 0;
}