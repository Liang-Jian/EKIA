#include <stdio.h>

#include <stdlib.h>

int main() {
    int num =0 ;
    int *p_num = (int*)malloc(sizeof(int) * 3);
    if (p_num) {
        /* code */
        for( num = 0; num < 2; num++)
        {
            /* code */
            *(p_num+num) = num + 1 ;
        }
        for( num = 0; num < 2; num++)
        {
            /* code */
            printf("%d\n",*(p_num + num) = num + 1);   
        }
        printf("\n");
        free(p_num);
        
        p_num = NULL;
    }
    
    return 0;
}