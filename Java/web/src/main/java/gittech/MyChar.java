package gittech;


class mychar{
    private  char ch;
    public mychar(char ch){this.ch = ch;}
    public boolean isvowel(){
        if (ch =='a' || ch=='A'){

            return true;
        }
        return false;
    }
    public boolean isdigit(){
        if (ch >= 32 && ch <=57)
            return true;
        return false;
    }
    public static void printLowerCaseAlphabets() {
        //'a' to 'z'
        for (char ch = 'a'; ch <= 'z'; ch++) {
            System.out.println(ch);
        }

        for (char ch ='a' ; ch <='z' ;ch++){
            System.out.println(ch);
        }
    }

}

public class MyChar {

    private char ch;

    public MyChar(char ch) {
        this.ch = ch;
    }

    public boolean isVowel() {
        //'a' e i o u or A E I O U
        if(ch == 'a' || ch == 'A')
            return true;

        if(ch == 'e' || ch == 'E')
            return true;

        if(ch == 'i' || ch == 'E')
            return true;

        if(ch == 'o' || ch == 'O')
            return true;

        if(ch == 'u' || ch == 'U')
            return true;

        return false;
    }

    public boolean isDigit() {
        if(ch >= 48 && ch <=57) //between '0' and '9'
            return true;

        return false;
    }

    public boolean isAlphabet() {
        if(ch >= 97 && ch <=122) //between 'a' and 'z'
            return true;

        if(ch >= 65 && ch <=90) //between 'A' and 'Z'
            return true;

        return false;
    }

    public boolean isConsonant() {
        //Alphabet and it is not VOWEL
        //! [a , e, i ,o , u]
        if(isAlphabet() && !isVowel())
            return true;

        return false;

    }

    public static void printLowerCaseAlphabets() {
        //'a' to 'z'
        for (char ch = 'a'; ch <= 'z'; ch++) {
            System.out.println(ch);
        }
    }

    public static void printUpperCaseAlphabets() {
        for (char ch = 'A'; ch <= 'Z'; ch++) {
            System.out.println(ch);
        }

    }
}

