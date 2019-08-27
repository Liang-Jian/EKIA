//
// Created by itw_shict on 2018/11/7.
//

#include <stdio.h>
int main(void)
{
    unsigned width,precision;
    int number = 235;
    double weight = 242.4;

    printf("What field width \n");
    scanf("%d",&width);
    printf("The number is :%*d: \n",width,number);

    printf("Now enter awidth and aprecision: \n");
    scanf("%d %d",&width,&precision);
    printf("Weight = %*.*f\n",width,precision,weight);

}


