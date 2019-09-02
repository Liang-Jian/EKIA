//
//
#include <string.h>
#include <stdio.h>

#include <fcntl.h>
#include <unistd.h>



#define BLURB  "Authentic imitation !"
int stringpring()
{
    printf("/%2s /\n", BLURB);
    printf("/%24s /\n", BLURB);
    printf("/%24.5s /\n", BLURB);
    printf("/%-24.5s /\n", BLURB);
    return 0;
}
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



int tb1()
{
    float a = 12.5;
    double b = 16.23;
    double c = 0.12312435435465464;
    printf("%g",a);
    printf("%f.5\n",c);
    char d = 'c';
    printf("c is %d\n",d);

    short a1=0;
    printf("%d",sizeof(a1));
    printf("%d",sizeof(short));

    int s1 = 0 , s2 = 0;
    printf("enerter sanjiaoxing");
    scanf("%d %d",&s1,&s2);
    int nu = s1 * s2 /2;
    printf("%d",nu);

    const int b1 =100;
    printf("%d",b1);
    int cc = 10;
    cc =++cc;
    printf("%d",cc);
    int k = 85;
    printf("%c",k);

    char ch = 'a';
    printf("%hhd",ch);

    printf("%010d ,%010d ",123,456);

    return 0;
}

int floaerr (){
    float a,b;
    b = 2.0e20 + 1.0;
    a = b -2.0e20;
    printf("%f \n", a);
    return 0;
}


#include <inttypes.h>

int altnames(){
    int16_t = mel6;
    mel6 =4594;
    printf("First,asssume itn16_t is short\n:", );
    printf("mel6 = %hd \n", mel6);
    printf("Next,let's not make any assumptions \n", );
    printf("Instead,use a \"macro\" from inttypes.h \n", );
    printf("mel6 = %" PRID16 "\n", mel6);
    return 0;
}

int lianhe() {
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

int meiju(){

    enum{C,X,S,D};//enum  leixing bu yong chushi ;
    // printf("%d\n",C);
    int arr = 0;
    printf("enter num\n");
    scanf("%d",&arr);
    if (arr==C){
        printf("chunt\n");
    }
    return 0;
}

int memshow() {
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

int striingtest(){
    char *fuck[5] = {"100","200","300","500","324"};
    int num = 0;
    for( num = 0; num <= 4; num++)
    {
        printf("%s\n",fuck[num]);
        /* code */
    }
    return 0;
}


int floats(){
    const double RENT = 3859.99; //以const 方法定义的常量
    printf("**%f *\n", RENT);
    printf("**%e *\n", RENT);
    printf("**%4.2f *\n", RENT);
    printf("**%3.1f *\n", RENT);
    printf("**%10.3f *\n", RENT);
    printf("**%10.3e *\n", RENT);
    printf("**%+4.2f *\n", RENT);
    printf("**%010.2f *\n", RENT);
    return 0;
}

int flags(int argc, char const *argv[])
{
    printf("%x %X %#x \n", 31,31,31);
    printf("***%d**% d ** % d **\n", 42,42,-42);
    printf("**%5d**%5.3d ** %05d ** %05.3d ** \n", 4,4,4,4);
    return 0;
}


int characdoe()
{
    char ch;
    printf("Please enter a character.\n", );
    scanf("%c",&ch);
    printf("The code  for %c is %d .\n", ch,ch);
    return 0;
}

int input()
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


void print1(){
    int ten = 10;
    int two = 2;
    printf("Doing it right \n", );
    printf("%d minus %d is %d \n", ten,2,ten-two);
    printf("Doing it wrong \n", );
    printf("%d  minus %d is %d \n", ten);
}

int showf(){
    float about = 32000.0;
    double bet = 2.13e9;
    long double dip = 5.32e-5;
    printf("%f can be writeen %e \n", about,about);
    printf("%f can be writeen %e \n", bet,bet);
    printf("%f can be writeen %e \n", dip,dip);

    return 0;
}

int printval(){
    int bph2o = 212;
    int rv;

    rv = printf("%d F is water 's boilling point \n", bph2o);
    printf("The printf() function printed %d characters;\n",rv);
    return 0;
}
void print2()
{
    unsigned int un = 30000000;
    short end = 200;
    long big = 65537;
    long long verybig = 1234567890864;
    printf("un =%u and not %d \n", un,un);
    printf("end=%hd and %d \n", end,end);
    printf("big=%ld and not %hd \n", big,big);
    printf("verybig =%lld and not %ld \n", verybig,verybig);
}

int toobig(){

    int i = 23425425435353;
    unsigned int j = 23423534543;

    printf("%d %d %d \n", i,i+1,i+2);
    printf("%u %u %u \n", j,j+1,j+2);
    return 0;
}

int varwid()
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


int ttalkback(){
    float weight,volume;
    int size,letters;
    char name[40];

    printf("Hi! what's you first name ?\n");
    scanf("%s",name);
    printf("%s,what's you weight in pounds?\n",name );
    scanf("%f",&weight);
    size = sizeof name;
    letters = strlen(name);
    volume = weight / DENSITY;

    printf("Well, %s ,your volume is %2.2f cubic feet.\n",name,volume );
    printf("Also,your first name has %d letters,\n", letters);
    printf("and we have %d bytes to store it in .\n", size );
    return 0;

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