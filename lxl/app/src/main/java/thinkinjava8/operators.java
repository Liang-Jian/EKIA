package thinkinjava8;

import java.util.*;


/*
*  Think in Java On J8  .
*  4 charpter .
*
s*/


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

class ShortCircuit{
    static boolean test1(int val) {
        System.out.println("test1(" + val + ")");
        System.out.println("result: " + (val < 1));
        return val < 1;
    }

    static boolean test2(int val) {
        System.out.println("test2(" + val + ")");
        System.out.println("result: " + (val < 2));
        return val < 2;
    }

    static boolean test3(int val) {
        System.out.println("test3(" + val + ")");
        System.out.println("result: " + (val < 3));
        return val < 3;
    }

    void f() {
        boolean b = test1(0) && test2(2) && test3(2);
        System.out.println("expression is " + b);
    }
}

class Literals{
    void f() {
        int i1 = 0x2f; // 16进制 (小写)
        System.out.println(
                "i1: " + Integer.toBinaryString(i1));
        int i2 = 0X2F; // 16进制 (大写)
        System.out.println(
                "i2: " + Integer.toBinaryString(i2));
        int i3 = 0177; // 8进制 (前导0)
        System.out.println(
                "i3: " + Integer.toBinaryString(i3));
        char c = 0xffff; // 最大 char 型16进制值
        System.out.println(
                "c: " + Integer.toBinaryString(c));
        byte b = 0x7f; // 最大 byte 型16进制值  01111111;
        System.out.println(
                "b: " + Integer.toBinaryString(b));
        short s = 0x7fff; // 最大 short 型16进制值
        System.out.println(
                "s: " + Integer.toBinaryString(s));
        long n1 = 200L; // long 型后缀
        long n2 = 200l; // long 型后缀 (容易与数值1混淆)
        long n3 = 200;

        // Java 7 二进制字面值常量:
        byte blb = (byte)0b00110101;
        System.out.println(
                "blb: " + Integer.toBinaryString(blb));
        short bls = (short)0B0010111110101111;
        System.out.println(
                "bls: " + Integer.toBinaryString(bls));
        int bli = 0b00101111101011111010111110101111;
        System.out.println(
                "bli: " + Integer.toBinaryString(bli));
        long bll = 0b00101111101011111010111110101111;
        System.out.println(
                "bll: " + Long.toBinaryString(bll));
        float f1 = 1;
        float f2 = 1F; // float 型后缀
        float f3 = 1f; // float 型后缀
        double d1 = 1d; // double 型后缀
        double d2 = 1D; // double 型后缀
        // (long 型的字面值同样适用于十六进制和8进制 )
    }
}


class Underscores{
    void f(){
        double d = 341_435_936.445_667;
        System.out.println(d);
        int bin = 0b0010_1111_1010_1111_1010_1111_1010_1111;
        System.out.println(Integer.toBinaryString(bin));
        System.out.printf("%x%n", bin); // [1]
        long hex = 0x7f_e9_b7_aa;
        System.out.printf("%x%n", hex);
    }
}


class  Exponents{
    void f(){
        // 大写 E 和小写 e 的效果相同:
        float expFloat = 1.39e-43f;
        expFloat = 1.39E-43f;
        System.out.println(expFloat);
        double expDouble = 47e47d; // 'd' 是可选的
        double expDouble2 = 47e47; // 自动转换为 double
        System.out.println(expDouble);
    }
}


class URShift{
    void f(){
        int i = -1;
        System.out.println(Integer.toBinaryString(i));
        i >>>= 10;
        System.out.println(Integer.toBinaryString(i));
        long l = -1;
        System.out.println(Long.toBinaryString(l));
        l >>>= 10;
        System.out.println(Long.toBinaryString(l));
        short s = -1;
        System.out.println(Integer.toBinaryString(s));
        s >>>= 10;
        System.out.println(Integer.toBinaryString(s));
        byte b = -1;
        System.out.println(Integer.toBinaryString(b));
        b >>>= 10;
        System.out.println(Integer.toBinaryString(b));
        b = -1;
        System.out.println(Integer.toBinaryString(b));
        System.out.println(Integer.toBinaryString(b>>>10));
    }
}


class BitManipulation{
    void f() {
        Random rand = new Random(47);
        int i = rand.nextInt();
        int j = rand.nextInt();
        printBinaryInt("-1", -1);
        printBinaryInt("+1", +1);
        int maxpos = 2147483647;
        printBinaryInt("maxpos", maxpos);
        int maxneg = -2147483648;
        printBinaryInt("maxneg", maxneg);
        printBinaryInt("i", i);
        printBinaryInt("~i", ~i);
        printBinaryInt("-i", -i);
        printBinaryInt("j", j);
        printBinaryInt("i & j", i & j);
        printBinaryInt("i | j", i | j);
        printBinaryInt("i ^ j", i ^ j);
        printBinaryInt("i << 5", i << 5);
        printBinaryInt("i >> 5", i >> 5);
        printBinaryInt("(~i) >> 5", (~i) >> 5);
        printBinaryInt("i >>> 5", i >>> 5);
        printBinaryInt("(~i) >>> 5", (~i) >>> 5);
        long l = rand.nextLong();
        long m = rand.nextLong();
        printBinaryLong("-1L", -1L);
        printBinaryLong("+1L", +1L);
        long ll = 9223372036854775807L;
        printBinaryLong("maxpos", ll);
        long lln = -9223372036854775808L;
        printBinaryLong("maxneg", lln);
        printBinaryLong("l", l);
        printBinaryLong("~l", ~l);
        printBinaryLong("-l", -l);
        printBinaryLong("m", m);
        printBinaryLong("l & m", l & m);
        printBinaryLong("l | m", l | m);
        printBinaryLong("l ^ m", l ^ m);
        printBinaryLong("l << 5", l << 5);
        printBinaryLong("l >> 5", l >> 5);
        printBinaryLong("(~l) >> 5", (~l) >> 5);
        printBinaryLong("l >>> 5", l >>> 5);
        printBinaryLong("(~l) >>> 5", (~l) >>> 5);
    }

    static void printBinaryInt(String s, int i) {
        System.out.println(
                s + ", int: " + i + ", binary:\n " +
                        Integer.toBinaryString(i));
    }

    static void printBinaryLong(String s, long l) {
        System.out.println(
                s + ", long: " + l + ", binary:\n " +
                        Long.toBinaryString(l));
    }
}

class TernaryIfElse{
    static int ternary(int i) {
        return i < 10 ? i * 100 : i * 10;
    }

    static int standardIfElse(int i) {
        if(i < 10)
            return i * 100;
        else
            return i * 10;
    }

    void f() {
        System.out.println(ternary(9));
        System.out.println(ternary(10));
        System.out.println(standardIfElse(9));
        System.out.println(standardIfElse(10));
    }
}


class StringOperators{
    void f(){
        int x = 0, y = 1, z = 2;
        String s = "x, y, z ";
        System.out.println(s + x + y + z);
        // 将 x 转换为字符串
        System.out.println(x + " " + s);
        s += "(summed) = ";
        // 级联操作
        System.out.println(s + (x + y + z));
        // Integer.toString()方法的简写:
        System.out.println("" + x);
    }
}


class CastingNumbers{
    void f(){
            double above = 0.7, below = 0.4;
            float fabove = 0.7f, fbelow = 0.4f;
            System.out.println("(int)above: " + (int)above);
            System.out.println("(int)below: " + (int)below);
            System.out.println("(int)fabove: " + (int)fabove);
            System.out.println("(int)fbelow: " + (int)fbelow);

    }
}


class Casting{ // 类型zhuanhuan
    void f(){
        int i = 200;
        long lng = (long)i;
        lng = i; // 没有必要的类型提升
        long lng2 = (long)200;
        lng2 = 200;
        // 类型收缩
        i = (int)lng2; // Cast required
        System.out.println(i);
    }
}


class RoundingNumbers{
    static void f() {
        double above = 0.7, below = 0.4;
        float fabove = 0.7f, fbelow = 0.4f;
        System.out.println("Math.round(above): "  + Math.round(above));
        System.out.println("Math.round(below): "  + Math.round(below));
        System.out.println("Math.round(fabove): " + Math.round(fabove));
        System.out.println("Math.round(fbelow): " + Math.round(fbelow));
    }
}


// operators/AllOps.java
// 测试所有基本类型的运算符操作
// 看看哪些是能被 Java 编译器接受的
class AllOps {
    // 布尔值的接收测试：
    void f(boolean b) {}
    void boolTest(boolean x, boolean y) {
        // 算数运算符：
        //- x = x * y;
        //- x = x / y;
        //- x = x % y;
        //- x = x + y;
        //- x = x - y;
        //- x++;
        //- x--;
        //- x = +y;
        //- x = -y;
        // 关系运算符和逻辑运算符：
        //- f(x > y);
        //- f(x >= y);
        //- f(x < y);
        //- f(x <= y);
        f(x == y);
        f(x != y);
        f(!y);
        x = x && y;
        x = x || y;
        // 按位运算符：
        //- x = ~y;
        x = x & y;
        x = x | y;
        x = x ^ y;
        //- x = x << 1;
        //- x = x >> 1;
        //- x = x >>> 1;
        // 联合赋值：
        //- x += y;
        //- x -= y;
        //- x *= y;
        //- x /= y;
        //- x %= y;
        //- x <<= 1;
        //- x >>= 1;
        //- x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换：
        //- char c = (char)x;
        //- byte b = (byte)x;
        //- short s = (short)x;
        //- int i = (int)x;
        //- long l = (long)x;
        //- float f = (float)x;
        //- double d = (double)x;
    }

    void charTest(char x, char y) {
        // 算数运算符：
        x = (char)(x * y);
        x = (char)(x / y);
        x = (char)(x % y);
        x = (char)(x + y);
        x = (char)(x - y);
        x++;
        x--;
        x = (char) + y;
        x = (char) - y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        x= (char)~y;
        x = (char)(x & y);
        x = (char)(x | y);
        x = (char)(x ^ y);
        x = (char)(x << 1);
        x = (char)(x >> 1);
        x = (char)(x >>> 1);
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        x <<= 1;
        x >>= 1;
        x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换
        //- boolean bl = (boolean)x;
        byte b = (byte)x;
        short s = (short)x;
        int i = (int)x;
        long l = (long)x;
        float f = (float)x;
        double d = (double)x;
    }

    void byteTest(byte x, byte y) {
        // 算数运算符：
        x = (byte)(x* y);
        x = (byte)(x / y);
        x = (byte)(x % y);
        x = (byte)(x + y);
        x = (byte)(x - y);
        x++;
        x--;
        x = (byte) + y;
        x = (byte) - y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        //按位运算符：
        x = (byte)~y;
        x = (byte)(x & y);
        x = (byte)(x | y);
        x = (byte)(x ^ y);
        x = (byte)(x << 1);
        x = (byte)(x >> 1);
        x = (byte)(x >>> 1);
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        x <<= 1;
        x >>= 1;
        x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        short s = (short)x;
        int i = (int)x;
        long l = (long)x;
        float f = (float)x;
        double d = (double)x;
    }

    void shortTest(short x, short y) {
        // 算术运算符：
        x = (short)(x * y);
        x = (short)(x / y);
        x = (short)(x % y);
        x = (short)(x + y);
        x = (short)(x - y);
        x++;
        x--;
        x = (short) + y;
        x = (short) - y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        x = (short) ~ y;
        x = (short)(x & y);
        x = (short)(x | y);
        x = (short)(x ^ y);
        x = (short)(x << 1);
        x = (short)(x >> 1);
        x = (short)(x >>> 1);
        // Compound assignment:
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        x <<= 1;
        x >>= 1;
        x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        byte b = (byte)x;
        int i = (int)x;
        long l = (long)x;
        float f = (float)x;
        double d = (double)x;
    }

    void intTest(int x, int y) {
        // 算术运算符：
        x = x * y;
        x = x / y;
        x = x % y;
        x = x + y;
        x = x - y;
        x++;
        x--;
        x = +y;
        x = -y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        x = ~y;
        x = x & y;
        x = x | y;
        x = x ^ y;
        x = x << 1;
        x = x >> 1;
        x = x >>> 1;
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        x <<= 1;
        x >>= 1;
        x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        byte b = (byte)x;
        short s = (short)x;
        long l = (long)x;
        float f = (float)x;
        double d = (double)x;
    }

    void longTest(long x, long y) {
        // 算数运算符：
        x = x * y;
        x = x / y;
        x = x % y;
        x = x + y;
        x = x - y;
        x++;
        x--;
        x = +y;
        x = -y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        x = ~y;
        x = x & y;
        x = x | y;
        x = x ^ y;
        x = x << 1;
        x = x >> 1;
        x = x >>> 1;
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        x <<= 1;
        x >>= 1;
        x >>>= 1;
        x &= y;
        x ^= y;
        x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        byte b = (byte)x;
        short s = (short)x;
        int i = (int)x;
        float f = (float)x;
        double d = (double)x;
    }

    void floatTest(float x, float y) {
        // 算数运算符：
        x = x * y;
        x = x / y;
        x = x % y;
        x = x + y;
        x = x - y;
        x++;
        x--;
        x = +y;
        x = -y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        //- x = ~y;
        //- x = x & y;
        //- x = x | y;
        //- x = x ^ y;
        //- x = x << 1;
        //- x = x >> 1;
        //- x = x >>> 1;
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        //- x <<= 1;
        //- x >>= 1;
        //- x >>>= 1;
        //- x &= y;
        //- x ^= y;
        //- x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        byte b = (byte)x;
        short s = (short)x;
        int i = (int)x;
        long l = (long)x;
        double d = (double)x;
    }

    void doubleTest(double x, double y) {
        // 算术运算符：
        x = x * y;
        x = x / y;
        x = x % y;
        x = x + y;
        x = x - y;
        x++;
        x--;
        x = +y;
        x = -y;
        // 关系和逻辑运算符：
        f(x > y);
        f(x >= y);
        f(x < y);
        f(x <= y);
        f(x == y);
        f(x != y);
        //- f(!x);
        //- f(x && y);
        //- f(x || y);
        // 按位运算符：
        //- x = ~y;
        //- x = x & y;
        //- x = x | y;
        //- x = x ^ y;
        //- x = x << 1;
        //- x = x >> 1;
        //- x = x >>> 1;
        // 联合赋值：
        x += y;
        x -= y;
        x *= y;
        x /= y;
        x %= y;
        //- x <<= 1;
        //- x >>= 1;
        //- x >>>= 1;
        //- x &= y;
        //- x ^= y;
        //- x |= y;
        // 类型转换：
        //- boolean bl = (boolean)x;
        char c = (char)x;
        byte b = (byte)x;
        short s = (short)x;
        int i = (int)x;
        long l = (long)x;
        float f = (float)x;
    }
}


class Overflow{ //类型转换
    static void f(){
        int big = Integer.MAX_VALUE;
        System.out.println("big = " + big);
        int bigger = big * 4;
        System.out.println("bigger = " + bigger);
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
//        EqualsMethod em = new EqualsMethod();
//        em.f();
//        EqualsMethod2 em2 = new EqualsMethod2();
//        em2.f();
//        Bool b = new Bool();
//        b.f();
//        ShortCircuit sc = new ShortCircuit();
//        sc.f();
//        Literals ls = new Literals();
//        ls.f();
//        Underscores us = new Underscores();
//        us.f();
//        Exponents es = new Exponents();
//        es.f();
//        URShift us = new URShift();
//        us.f();
//        BitManipulation bm = new BitManipulation();
//        bm.f();
//        TernaryIfElse ti = new TernaryIfElse();
//        ti.f();
//        StringOperators so = new StringOperators();
//        so.f();
//        Casting ci = new Casting();
//        ci.f();

//        CastingNumbers cn = new CastingNumbers();
//        cn.f();
//        RoundingNumbers.f();
//        CastingNumbers cn1 = new CastingNumbers();
//        cn1.f();
        Overflow.f();
    }
}
