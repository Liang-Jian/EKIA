
#include <stdio.h>
#include <stdlib.h> //touwenjian
#include <time.h>

/*

int main() {

    srand(time(0));
    int arr[7], num = 0;

    for (int num = 0; num <=6 ; num++) {
        arr[num] = 0;
    }
    for (int num = 0; num <=6; num++) {
        arr[num] = rand() % 6 == 1;
    }
    for (int num = 0; num < 6; num++) {
        printf("%d  ",arr[num]);
    }

}
*/


/*
int main()
{

    int num[10],wol = 0 ,col = 0 ;
    for (int wol = 0; wol < 9; wol++) {
        printf("enter numb");
        scanf("%d",&num[wol]);
        printf("\n");
    }
    for (int wol = 0; wol < 9; wol++) {
        col = num[wol] > num[wol +1 ] ? num[wol] :num[wol +1 ];
    }

    printf("Max int %d\n", col);
    return  0;


}*/


void fuckworld()
{
    printf("fuckworld");
    printf("fuckworld");

}


//    void print();
//    print();
//    int sct();
//    sct();
//    printf("%d\n",sct());
//
//    int num = 0;
//    int cadillac(int x, int y);
//    num = cadillac(3,4);
//    printf("%d\n",num);
//    int max = 0, min = 0 ,col = 0;
//    int Fetters(int x, int y);
//    printf("please enter number\n");
//    scanf("%d %d",&max,&min);
//    col = Fetters(max,min);
//    printf("max number is %d \n",col);
//    void name();
//    fuckworld();
//    name();
//    return 0;
/*

    int arr[10], num = 0;
    void max(int arr[],int num);
    max(arr,6);
    for (int num = 0; num <=5; num++) {
        printf("%d\n",arr[num]);
    }
*/

/*    int arr[2]  =  {0,0};
    FILE *p_file = fopen("a.txt","w");
    if (!p_file){
        printf("file open failed\n");
        return 0;
    }

    fwrite(arr, sizeof(int),1,p_file);
    fclose(p_file);
    p_file = NULL;

    return 0;*/

//
//void print(){
//    printf("use this void");
//}
//
//int sct()
//{
//    int num = 3;
//    int num1 = 4;
//    int k = 0;
//    k = num + num1;
//    return k;
//}

//
//int cadillac(int x , int y)
//{
//    int z = 0; //函数不能初始化
//    z = x + y ;
//    return z;
//
//}

//int Fetters(int x, int y)
//{
//    int z = 0 ;
//    z = x < y ? y : x;
//    return z;
//}


/*
void name()
{
    printf("Hello World\n");
    exit(0);
    printf("Hello World\n");

}

void max(int arr[], int num)
{
    int z = 0;
    for (int z = 0; z <= 6; z++)
    {
        arr[z] = 9;
    }
}*/


/*

//复制文件
int main()
{
    char buf[120] = {};
    int size = 0 ;
    FILE *f_src = fopen("abc.txt","rb");  //读取的方式打开文件
    if(!f_src){ //如果不存在，报错
        printf("Nopen*Fail");
        return 0;
    }
    FILE *p_dst = fopen("def.txt","wb");
    if(!p_dst){//同上
        printf("Dfile*Fail");
        return 0;
    }

    while (size = fread(buf, sizeof(char),128,f_src)) //当读取不到文件时。
    {
        fwrite(buf, sizeof(char),size,p_dst); //写入文件

    }
    fclose(p_dst); // 关闭文件
    p_dst = NULL; // 将内存置空
    fclose(f_src);
    f_src = NULL;

    return 0;
}
*/


/*

//递归调用。传入初始值，
int sum(int num){
    printf("1\n"); //显示迭代过程
    if (num ==0){ //
        return 0;
    }
    sum(num -1);
}
int main()
{
    sum(10);
    return 0;
}
*/

/*

int f()
{
    static int num = 10; //static声明静态变量 。只生命一次。
    printf("num is %d\n",num);
    num =3 ;
}

{
    f();
    f();
    return 0;
}
*/
/*

{
    volatile int i = 10;  //volatile 用来生命多变变量。内容随时可能会改变
    int j = i;
    int k =i;
    printf("1 is %d, j is %d,k is %d",i,j,k);
    return 0;
}
*/
/*

int main()
{
    int num =0 ,num1 = 0 , num2 = 0;
    int *p_num = &num;
    int *p_num1 = &num1;
    int *p_num2 = &num2;
    printf("enter nuber");
    scanf("%d %d %d", &num,&num1,&num2);
    if (*p_num < *p_num1)  //使用指针来判断大小。
    {
        *p_num += *p_num1;
        *p_num1 = *p_num - *p_num1;
        *p_num  = *p_num - *p_num1;
    }
    if (*p_num < *p_num2)
    {
        *p_num += *p_num2;
        *p_num2 = *p_num - *p_num2;
        *p_num  = *p_num - *p_num2;

    }
    printf("%d\n",*p_num);
    return 0;
}
*/
/*
int main()
{
    int num=0 , num1 = 0 , num2 =0;
    int *p_num = &num , *p_num1 = &num1 , *p_num2 = &num2;
    printf("enter number:");
    scanf("%d %d %d",p_num,p_num1,p_num2);
    if (*p_num < *p_num1)
    {
        int *p_tmp = p_num;
        p_num = p_num1;
        p_num1 = p_tmp;
    }

    if (*p_num < *p_num2)
    {
        int *tmp = p_num;
        p_num = p_num2;
        p_num2 = p_tmp;
    }
    if (*p_num1 < *p_num2)
    {
        int *tmp = p_num2;
        p_num1 = p_num2;
        p_num2 = p_tmp;
    }
    printf("%d %d %d\n",*p_num,*p_num1,*p_num2);
    return 0 ;
}
*/

int bases(){
	int x= 100;
	printf("dec = %d;octal = %o;hex=%x\n", x,x,x );
	printf("dec = %d;octal = %#o;hex=%#x\n", x,x,x);
	return 0;
	// printf("%s\n", );
}

int main()
{
    int num =0 ; num1 = 0 ;num2 = 0 ;

}

