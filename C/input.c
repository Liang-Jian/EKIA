//
// Created by itw_shict on 2018/11/6.
//

#include <stdio.h>

int main(void)
{
    int age;

    float assets;
    char pet[30];

    printf("Enter you age,assets,and favorite pet. \n");
    scanf("%d %f",&age,&assets);
    scanf("%s",pet);
    printf("%d $%.2f %s \n",age,assets,pet);
    return 0;
}
