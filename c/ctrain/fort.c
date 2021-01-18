//
// Created by lexue on 2020/11/2.
//

#include <stdio.h>
#define LOWER 0
#define UPPER 300
#define STEP 20

/**
 * #define 符合常量
 * #define 名字 替换文本
 *
 *
 * @return
 */
int forta(){

    int j;
    for (int j = LOWER; j < UPPER; j = j *STEP) {
        printf("%3d %6.1f\n",j,(5.0/9.0) * (j -32));

    }
    return 0;
}


