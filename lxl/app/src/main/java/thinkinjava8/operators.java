package thinkinjava8;

import java.util.*;


// 9/21/2020
class Precedence{
    void f() {
        int x = 1, y = 2, z = 3;
        int a = x + y - 2/2 + z; // [1]
        int b = x + (y - 2)/(2 + z); // [2]
        System.out.println("a = " + a);
        System.out.println("b = " + b);
    }
}

class Tank{ int level;}
class Assignment{
    void f() {
        Tank t1 = new Tank();
        Tank t2 = new Tank();
        t1.level = 9;
        t2.level = 47;
        System.out.println("1: t1.level: " + t1.level +
                ", t2.level: " + t2.level);
        t1 = t2;
        System.out.println("2: t1.level: " + t1.level +
                ", t2.level: " + t2.level);
        t1.level = 27;
        System.out.println("3: t1.level: " + t1.level +
                ", t2.level: " + t2.level);
    }
}

class Letter{
    char c;
}
class PassObject{
    static void f(Letter y){
        y.c = 'z';
    }
    void f(){
        Letter x = new Letter();
        x.c = 'a';
        System.out.println("1: x.c: " + x.c);
        f(x);
        System.out.println("2: x.c: " + x.c);
    }
}


class MathOps{
    void f() {
        // Create a seeded random number generator:
        Random rand = new Random(47);
        int i, j, k;
        // Choose value from 1 to 100:
        j = rand.nextInt(100) + 1;
        System.out.println("j : " + j);
        k = rand.nextInt(100) + 1;
        System.out.println("k : " + k);
        i = j + k;
        System.out.println("j + k : " + i);
        i = j - k;
        System.out.println("j - k : " + i);
        i = k / j;
        System.out.println("k / j : " + i);
        i = k * j;
        System.out.println("k * j : " + i);
        i = k % j;
        System.out.println("k % j : " + i);
        j %= k;
        System.out.println("j %= k : " + j);
        // 浮点运算测试
        float u, v, w; // Applies to doubles, too
        v = rand.nextFloat();
        System.out.println("v : " + v);
        w = rand.nextFloat();
        System.out.println("w : " + w);
        u = v + w;
        System.out.println("v + w : " + u);
        u = v - w;
        System.out.println("v - w : " + u);
        u = v * w;
        System.out.println("v * w : " + u);
        u = v / w;
        System.out.println("v / w : " + u);
        // 下面的操作同样适用于 char,
        // byte, short, int, long, and double:
        u += v;
        System.out.println("u += v : " + u);
        u -= v;
        System.out.println("u -= v : " + u);
        u *= v;
        System.out.println("u *= v : " + u);
        u /= v;
        System.out.println("u /= v : " + u);
    }
}


//
class AutoInc{
    void f(){
        int i = 1;
        System.out.println("i: " + i);
        System.out.println("++i: " + ++i); // 前递增
        System.out.println("i++: " + i++); // 后递增
        System.out.println("i: " + i);
        System.out.println("--i: " + --i); // 前递减
        System.out.println("i--: " + i--); // 后递减
        System.out.println("i: " + i);
    }
}


class Equivalence{
    void f(){
        Integer n1 = 47;
        Integer n2 = 47;
        System.out.println(n1 == n2);
        System.out.println(n1 != n2);
    }
}

class EqualsMethod{
    void f(){
        Integer n1 = 47;
        Integer n2 = 47;
        System.out.println(n1.equals(n2));
    }
}


class Value {
    int i;
}
class EqualsMethod2 {
    void f() {
        Value v1 = new Value();
        Value v2 = new Value();
        v1.i = v2.i = 100;
        System.out.println(v1.equals(v2));
    }
}

class Bool{
    void f() {
        Random rand = new Random(47);
        int i = rand.nextInt(100);
        int j = rand.nextInt(100);
        System.out.println("i = " + i);
        System.out.println("j = " + j);
        System.out.println("i > j is " + (i > j));
        System.out.println("i < j is " + (i < j));
        System.out.println("i >= j is " + (i >= j));
        System.out.println("i <= j is " + (i <= j));
        System.out.println("i == j is " + (i == j));
        System.out.println("i != j is " + (i != j));
        // 将 int 作为布尔处理不是合法的 Java 写法
        //- System.out.println("i && j is " + (i && j));
        //- System.out.println("i || j is " + (i || j));
        //- System.out.println("!i is " + !i);
        System.out.println("(i < 10) && (j < 10) is " + ((i < 10) && (j < 10)) );

        System.out.println("(i < 10) || (j < 10) is " + ((i < 10) || (j < 10)) );

    }
}




















public class operators {
    public static void main(String[] args) {
//        Precedence pr = new Precedence();
//        pr.f();
//        Assignment as = new Assignment();
//        as.f();
//        PassObject po = new PassObject();
//        po.f();
//        MathOps mo = new MathOps();
//        mo.f();
//        AutoInc ai = new AutoInc();
//        ai.f();
//        Equivalence ev = new Equivalence();
//        ev.f();
        EqualsMethod em = new EqualsMethod();
        em.f();
        EqualsMethod2 em2 = new EqualsMethod2();
        em2.f();
        Bool b = new Bool();
        b.f();

    }
}
