package thinkinjava8;
import java.sql.Array;
import java.util.*;
//import static java.util.*;
/*
*  控制流
*  5 chapter
*
*
*/


class TrueFalse{
    static void f(){
        System.out.println(1 == 1);
        System.out.println(1 == 2);
    }
}


class IfElse{
    static int result = 0;
    static void test(int testval, int target) {
        if(testval > target)
            result = +1;
        else if(testval < target) // [1]
            result = -1;
        else
            result = 0; // Match
    }

    static void f() {
        test(10, 5);
        System.out.println(result);
        test(5, 10);
        System.out.println(result);
        test(5, 5);
        System.out.println(result);
    }
}


class WhileTest{
    static boolean condition() {
        boolean result = Math.random() < 0.99;
        System.out.print(result + ", ");
        return result;
    }
    static void f() {
        while(condition())
            System.out.println("Inside 'while'");
        System.out.println("Exited 'while'");
    }
}



class ListCharacters{
    static void f() {
        for(char c = 0; c < 128; c++)
            if(Character.isLowerCase(c))
                System.out.println("value: " + (int)c +  " character: " + c);
    }
}


class CommaOperator{
    static void f() {
        for(int i = 1, j = i + 10; i < 5; i++, j = i * 2) {
            System.out.println("i = " + i + " j = " + j);
        }
    }
}


class ForInFloat{
    static void f() {
        Random rand = new Random(47);
        float[] f = new float[10];
        for(int i = 0; i < 10; i++)
            f[i] = rand.nextFloat();
        for(float x : f)
            System.out.println(x);
    }
}


class ForInString{
    static void f() {
        for (char c : "An African Swallow".toCharArray())
            System.out.print(c + " ");
    }
}



/*class ForInInt{
    static void f() {
        for(int i : range(10)) // 0..9
            System.out.print(i + " ");
        System.out.println();
        for(int i : range(5, 10)) // 5..9
            System.out.print(i + " ");
        System.out.println();
        for(int i : range(5, 20, 3)) // 5..20 step 3
            System.out.print(i + " ");
        System.out.println();
        for(int i : range(20, 5, -3)) // Count down
            System.out.print(i + " ");
        System.out.println();
    }
}*/



class TestWithReturn{
    static int test(int testval, int target) {
        if(testval > target)
            return +1;
        if(testval < target)
            return -1;
        return 0; // Match
    }

    static void f() {
        System.out.println(test(10, 5));
        System.out.println(test(5, 10));
        System.out.println(test(5, 5));
    }
}



/*class BreakAndContinue{
    static void f() {
        for(int i = 0; i < 100; i++) { // [1]
            if(i == 74) break; // 跳出循环
            if(i % 9 != 0) continue; // 下一次循环
            System.out.print(i + " ");
        }
        System.out.println();
        // 使用 for-in 循环:
        for(int i : range(100)) { // [2]
            if(i == 74) break; // 跳出循环
            if(i % 9 != 0) continue; // 下一次循环
            System.out.print(i + " ");
        }
        System.out.println();
        int i = 0;
        //  "无限循环":
        while(true) { // [3]
            i++;
            int j = i * 27;
            if(j == 1269) break; // 跳出循环
            if(i % 10 != 0) continue; // 循环顶部
            System.out.print(i + " ");
        }
    }
}*/


class LabeledFor{
    static void f() {
        int i = 0;
        outer: // 此处不允许存在执行语句
        for(; true ;) { // 无限循环
            inner: // 此处不允许存在执行语句
            for(; i < 10; i++) {
                System.out.println("i = " + i);
                if(i == 2) {
                    System.out.println("continue");
                    continue;
                }
                if(i == 3) {
                    System.out.println("break");
                    i++; // 否则 i 永远无法获得自增
                    // 获得自增
                    break;
                }
                if(i == 7) {
                    System.out.println("continue outer");
                    i++;  // 否则 i 永远无法获得自增
                    // 获得自增
                    continue outer;
                }
                if(i == 8) {
                    System.out.println("break outer");
                    break outer;
                }
                for(int k = 0; k < 5; k++) {
                    if(k == 3) {
                        System.out.println("continue inner");
                        continue inner;
                    }
                }
            }
        }
        // 在此处无法 break 或 continue 标签
    }
}


class LabeledWhile{
    static void f() {
        int i = 0;
        outer:
        while(true) {
            System.out.println("Outer while loop");
            while(true) {
                i++;
                System.out.println("i = " + i);
                if(i == 1) {
                    System.out.println("continue");
                    continue;
                }
                if(i == 3) {
                    System.out.println("continue outer");
                    continue outer;
                }
                if(i == 5) {
                    System.out.println("break");
                    break;
                }
                if(i == 7) {
                    System.out.println("break outer");
                    break outer;
                }
            }
        }
    }
}


class VowelsAndConsonants{
    static void f() {
        Random rand = new Random(47);
        for(int i = 0; i < 100; i++) {
            int c = rand.nextInt(26) + 'a';
            System.out.print((char)c + ", " + c + ": ");
            switch(c) {
                case 'a':
                case 'e':
                case 'i':
                case 'o':
                case 'u': System.out.println("vowel");
                    break;
                case 'y':
                case 'w': System.out.println("Sometimes vowel");
                    break;
                default:  System.out.println("consonant");
            }
        }
    }
}


class StringSwitch{
    static void f() {
        String color = "red";
        // 老的方式: 使用 if-then 判断
        if("red".equals(color)) {
            System.out.println("RED");
        } else if("green".equals(color)) {
            System.out.println("GREEN");
        } else if("blue".equals(color)) {
            System.out.println("BLUE");
        } else if("yellow".equals(color)) {
            System.out.println("YELLOW");
        } else {
            System.out.println("Unknown");
        }
        // 新的方法: 字符串搭配 switch
        switch(color) {
            case "red":
                System.out.println("RED");
                break;
            case "green":
                System.out.println("GREEN");
                break;
            case "blue":
                System.out.println("BLUE");
                break;
            case "yellow":
                System.out.println("YELLOW");
                break;
            default:
                System.out.println("Unknown");
                break;
        }
    }
}



class RandomBounds{
    static   void f(String[] args) {
//        new TimedAbort(3);
        switch (args.length == 0 ? "" : args[0]) {
            case "lower":
                while (Math.random() != 0.0)
                    ; // 保持重试
                System.out.println("Produced 0.0!");
                break;
            case "upper":
                while (Math.random() != 1.0)
                    ; // 保持重试
                System.out.println("Produced 1.0!");
                break;
            default:
                System.out.println("Usage:");
                System.out.println("\tRandomBounds lower");
                System.out.println("\tRandomBounds upper");
                System.exit(1);
        }
    }
}












public class controlflow {
    public static void main(String[] args) {
//        TrueFalse.f();
//        IfElse.f();
//        WhileTest.f();
//        ListCharacters.f();
//        CommaOperator.f();
//        ForInFloat.f();
//        ForInString.f();
//        TestWithReturn.f();
//        LabeledFor.f();
//        LabeledWhile.f();
//        VowelsAndConsonants.f();
//        StringSwitch.f();
//        RandomBounds.f();

    }
}
