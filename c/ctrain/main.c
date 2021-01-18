//
// Created by lexue on 2020/11/3.
//

#include <stdio.h>
#include <string.h>
#include <ctype.h>

/*

#define MAXLINE 1000
enum boolean {NO,YES};
enum escapes {BelL = '\a',BACKSPACe= '\b'};
#define VTAB '\013'
#define BELL '\007'
#define LEAP 1


const double e = 2.54535365919084234;
const char msg[] = "warning";

int getline(char line[],int maxline);
void copy(char to[],char from[]);
int binsearch(int x, int v[] ,int n);

int main(){
    int a[10];
    binsearch(1,a,3);
    return 0;
}
int getline(char s[] , int lim){
    int c,i;
    for (int i = 0; i < lim - 1 && ( c =getchar()) != EOF && c !='\n'; ++i)
        s[i] = c;

    if (c == '\n'){
        s[i] = c;
        ++i;
    }
    s[i] = '\n';

    return 0;
}

void copy(char to[],char from[]){
    int i;
    i = 0;
    while ((to[i] = from[i]) != '\n')
        ++i;
}


//

int strlen1(char s[]){

    char esc = '\\';
    int i1 =0 ;
    int limit = MAXLINE + 1;
    float eps = 1.0e-1;
    int i;
    i = 0;
    while (s[i] != '\0')
        ++i;
    return 0;
}

int atoi(char s[]){

    int i,n;
    n = 0;
    for(i=0 ; s[i] >='0' && s[i] <= '9'; ++i)
        n = 10 * n +(s[i] - '0');
    return n;
}


int binsearch(int x, int v[] ,int n){
    int low,high,mid;
    low =0;
    high =n -1;
    while (low <= high){

        mid = (low + high) / 2 ;
        if (x < v[mid])
            high = mid -1 ;
        else if ( x > v[mid])
            low = mid + 1;
        else
            return mid;
    }
    return -1;

}


void shellsort(int v[], int n){
    int gap, i , j ,temp;
    for (int gap = 2; gap > 0 ; ++gap /=2) {

    }


}*/


#define MAXLINE 1000
int max;
char line[MAXLINE];
char longest[MAXLINE];
int getline(void);
void copy();
int lower();
int f();
//int atoi;


int main(){
    int len;
    char l[] = {'a','b','c'};
//    int kk = atoi(l);
//    f();
//    int sct = 23;
//    printf("fuck world\n");
//    int sd = lower(sct);
//    printf("%d\n",sd);
    return 0;
}
int getline(void ){

    int c , i;
    extern char line[];
    for (i = 0; i < MAXLINE -1 && (c =getchar()) !=EOF  && c != '\n'; ++i)
        line[i] = c;
    if (c == '\n'){
        line[i] =c ;
        ++i;
    }
    line[i] = '\0';
    return i;
}
void copy(){
    int i ;
    extern char line[],longest[];
    i = 0;
    while ((longest[i]  = line[i])  != '\0')
        ++i;

}


//int atoi(char s[]){
//
//    int i, n ;
//    n = 0 ;
//    for (i = 0; s[0] >= '0' && s[i] <= '9'; ++i ) {
//        n = 10 * n + (s[i] - '0');
//    }
//    return n;
//
//}


int lower(int c){
    if (c >= 'A' && c <= 'Z')
        return c + 'a' - 'A';
    else
        return c;
}


// page 444
void strcat_self(char s[], char t[]){
    int i, j;
    i =j = 0;
    while (s[i] != '\0')
        i++;
    while ((s[i++] = t[j++]) != '\0')
        ;

}


// page 47
int binsearch(int x, int v[] , int n)
{
    int low ,high,mid;

    low =0;
    high = n -1;
    while (low <= high){
        mid = (low + high)  / 2;
        if (x < v[mid])
            high = mid -1;
        else if  (x > v[mid])
            low  = mid + 1;
        else
            return mid;
    }
    return -1;
}



int f(){

    int c, i, nwhite, nother,ndigit[10];
    nwhite = nother = 0;
    for (i =0 ; i < 10 ;i++)
        ndigit[i] =0;

    while ((c = getchar()) != EOF){
        switch (c){
            case '0' : case '1' : case '2' : case '3' : case '4' :
            case '5' : case '6' : case '7' : case '8' : case '9' :
                ndigit[c - '0']++;
                break;
            case ' ' :
            case '\n' :
            case '\t' :
                nwhite++;
                break;

            default:
                nother++;
                break;
        }
    }
    printf("digits=");
    for (int j = 0; j < 10; ++j) {
        printf(" %d",ndigit[i]);
    }
    printf(", white spce = %d, other = %d\n",nwhite,nother);
    return 0;
}



// page51
void shellsort(int v[],int n)
{
    int gap, i , j ,temp;
    for (gap = n / 2; gap > 0; gap /=2)
    {
        for (i  = 0;  i< n; i++) {
            for (j = i - gap; j >=0 && v[j] > v[j+gap] ; j-=gap) {
                temp= v[j];
                v[j] = v[j + gap];
                v[j + gap] = temp;
            }
        }
    }
}



int trim(char s[])
{
    int n;
    for (n = strlen(s)-1; n >= 0 ; n--)
    {
        if (s[n] != ' ' && s[n] !='\t' && s[n] != '\n')
            break;
    }
    s[n +1 ] = '\0';
    return n;
}



int strindex(char s[], char t[])
{
    int i, j , k;
    for (i = 0 ; s[i] != '\0' && s[j] == t[k] ; j++, k++){
        ;
        if ( k > 0 && t[k] == '\0')
            return i;
    }
    return -1;
}




int cals()
{
    double sum,atof(char []);
    char line[MAXLINE];
    int getline(char line[],int max);

    sum = 0;
    while (getline(line,MAXLINE) > 0)
        printf("\t%g \n",sum += atof(line));
    return 0;
}



double atof(char s[])
{
    double val,power;
    int i, sign;
    for ( i =0 ; isspace(s[i])) i++);
}




