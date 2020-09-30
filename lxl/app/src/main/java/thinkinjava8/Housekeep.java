package thinkinjava8;


/*
*
*   6 chapter
*   初始化和清理
*   Must be write use hand
*
* */

import java.util.Arrays;
import java.util.Random;

class Rock{
    Rock(){
        System.out.print("Rock");
    }
    Rock(int i){
        System.out.println("Rock " + i + " ");
    }
}
class SimpleConstructor{
    static void f(){
        for (int i = 0 ; i < 10 ; i++){
            new Rock();
        }
        for (int i = 0 ; i < 10 ; i++){
            new Rock(i);
        }
    }
}



class Tree{
    int height;
    Tree(){
        System.out.println("planting a tree");
        height = 0;
    }
    Tree(int initialHeight){
        height = initialHeight;
        System.out.println("Creating new Tree that is " + height + " feet tall");
    }
    void info(){
        System.out.println("Tree is " + height + " feet tall");
    }
    void info(String s ){
        System.out.println(s + ": Tree is " + height + " feet tall");
    }

    static  void f(){
        for (int i = 0 ; i < 5 ;i++){
            Tree t =  new Tree(i);
            t.info();
            t.info("fuck the world");
        }
        new Tree();
    }
}



class OverloadingOrder{
    static void f(String s , int i ){
        System.out.println("String: "  +s  + ", int: " + i);
    }
    static void f(int i , String s ){
        System.out.println("int: " + i + ", String: " + s);
    }
    void t(){
        f(0x01,"fuck");
        f("fuck",365);
    }
}



class PrimitiveOverloading{ //基本类型 提升
    void f1(char x ){
        System.out.println("f1(char)");
    }
    void f1(byte b){
        System.out.println("f1(byte)");
    }
    void f1(short x) {
        System.out.print("f1(short)");
    }
    void f1(int x) {
        System.out.print("f1(int)");
    }
    void f1(long x) {
        System.out.print("f1(long)");
    }
    void f1(float x) {
        System.out.print("f1(float)");
    }
    void f1(double x) {
        System.out.print("f1(double)");
    }
    void f2(byte x) {
        System.out.print("f2(byte)");
    }
    void f2(short x) {
        System.out.print("f2(short)");
    }
    void f2(int x) {
        System.out.print("f2(int)");
    }
    void f2(long x) {
        System.out.print("f2(long)");
    }
    void f2(float x) {
        System.out.print("f2(float)");
    }
    void f2(double x) {
        System.out.print("f2(double)");
    }
    void f3(short x) {
        System.out.print("f3(short)");
    }
    void f3(int x) {
        System.out.print("f3(int)");
    }
    void f3(long x) {
        System.out.print("f3(long)");
    }
    void f3(float x) {
        System.out.print("f3(float)");
    }
    void f3(double x) {
        System.out.print("f3(double)");
    }
    void f4(int x) {
        System.out.print("f4(int)");
    }
    void f4(long x) {
        System.out.print("f4(long)");
    }
    void f4(float x) {
        System.out.print("f4(float)");
    }
    void f4(double x) {
        System.out.print("f4(double)");
    }
    void f5(long x) {
        System.out.print("f5(long)");
    }
    void f5(float x) {
        System.out.print("f5(float)");
    }
    void f5(double x) {
        System.out.print("f5(double)");
    }
    void f6(float x) {
        System.out.print("f6(float)");
    }
    void f6(double x) {
        System.out.print("f6(double)");
    }
    void f7(double x) {
        System.out.print("f7(double)");
    }
    void testConstVal() {
        System.out.print("5: ");
        f1(5);f2(5);f3(5);f4(5);f5(5);f6(5);f7(5);
        System.out.println();
    }
    void testChar() {
        char x = 'x';
        System.out.print("char: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testByte() {
        byte x = 0;
        System.out.print("byte: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testShort() {
        short x = 0;
        System.out.print("short: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testInt() {
        int x = 0;
        System.out.print("int: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testLong() {
        long x = 0;
        System.out.print("long: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testFloat() {
        float x = 0;
        System.out.print("float: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }
    void testDouble() {
        double x = 0;
        System.out.print("double: ");
        f1(x);f2(x);f3(x);f4(x);f5(x);f6(x);f7(x);
        System.out.println();
    }


     void f(){
        this.testConstVal();
        this.testChar();
        this.testByte();
        this.testShort();
        this.testInt();
        this.testLong();
        this.testFloat();
        this.testDouble();
    }
}


class Bird {}
class DefaultConstructor{
    static void f(){
        Bird b  = new Bird();
    }
}
class Bird2 {
    Bird2(int i){}
    Bird2(double d) {}
}
class NoSynthesis{
    static void f(){
        //- Bird2 b = new Bird2(); // No default
        Bird2 b2 = new Bird2(1);
        Bird2 b3 = new Bird2(1.0);
    }
}


class Banana {
    void peel(int i) {
        /*...*/
    }
}
class BananaPeel{
    static void f(){
        Banana a = new Banana(), b = new Banana();
        a.peel(1);
        b.peel(2);
    }
}


class Apricot{
    void pick(){}
    void pit(){
        pick();
    }
}
class Leaf{
    int i = 0 ;
    Leaf increament(){
        i++;
        return this;
    }
    void print() {
        System.out.println("i = " + i);
    }
    void f(){
        Leaf x = new Leaf();
        x.increament().increament().increament();
    }
}



class Person {
    public void eat(Apple apple) {
        Apple peeled = apple.getPeeled();
        System.out.println("Yummy");
    }
}

class Peeler {
    static Apple peel(Apple apple) {
        // ... remove peel
        return apple; // Peeled
    }
}

class Apple {
    Apple getPeeled() {
        return Peeler.peel(this);
    }
}

class PassingThis{
    void f(){
        new Person().eat(new Apple());
    }
}


class Flower{
    int petalCount = 0 ;
    String s = "initial value";

    Flower(int petals){
        petalCount = petals;
        System.out.println("Constructor w/ int arg only, petalCount = " + petalCount);
    }
    Flower(String ss){
        System.out.println("Constructor w/ string arg only, s = " + ss);
        s = ss;
    }
    Flower(String s, int petals){
        this(petals);
        this.s = s;
        System.out.println("String & int args");
    }
    Flower(){
        this("hi", 47);
        System.out.println("no-arg constructor");
    }
    void printPetalCount(){
        System.out.println("petalCount = " + petalCount + " s = " + s);
    }
    void f(){
        Flower x = new Flower();
        x.printPetalCount();
    }
}


class Book{
    boolean checkedOut = false;
    Book(boolean checkout){
        checkout = checkedOut;
    }
    void checkIn(){
        checkedOut = false;
    }
    @Override
    protected void finalize() throws Throwable {
        if (checkedOut) {
            System.out.println("Error: checked out");
        }
        // Normally, you'll also do this:
        // super.finalize(); // Call the base-class version
    }
}
class TerminationCondition{
    static void f(){
        Book novel = new Book(true);
        // Proper cleanup:
        novel.checkIn();
        // Drop the reference, forget to clean up:
        new Book(true);
        // Force garbage collection & finalization:
        System.gc();
//        new Nap(1); // One second delay
    }
}
















class InitialValues{
    boolean t;
    char c;
    byte b;
    short s;
    int i;
    long l;
    float f;
    double d;
    InitialValues reference;
    void printInitialValues() {
        System.out.println("Data type Initial value");
        System.out.println("boolean " + t);
        System.out.println("char[" + c + "]");
        System.out.println("byte " + b);
        System.out.println("short " + s);
        System.out.println("int " + i);
        System.out.println("long " + l);
        System.out.println("float " + f);
        System.out.println("double " + d);
        System.out.println("reference " + reference);
    }

    static void f(){
        new InitialValues().printInitialValues();
    }
}


class InitialValues2{
    boolean bool = true;
    char ch = 'x';
    byte b = 47;
    short s = 0xff;
    int i = 999;
    long lng = 1;
    float f = 3.14f;
    double d = 3.14159;
}
class Depth{}
class Measurement{
    Depth d = new Depth();
}


class MethodInit{
    int i = f();
    int f(){
        return 11;
    }
}
class MethodInit2{
    int i = f();
    int j = g(i);
    int f(){
        return 11;
    }
    int g(int n){
        return n * 10;
    }
}


class Counter{
    int i ;
    Counter(){
        i = 7;
    }
}

class Window{
    Window(int marker){
        System.out.println("Window(" + marker + ")");
    }
}
class House{
    Window w1  = new Window(1);
    House(){
        System.out.println("House");
        w3 = new Window(33);
    }
    Window w2 = new Window(2); // After constructor
    void f(){
        System.out.println("f()");
    }
    Window w3 = new Window(3); // At end
}
class OrderOfInitialization{
    void f(){
        House h = new House();
        h.f(); // Shows that construction is done
    }
}


class Bowl{
    Bowl(int marker){
        System.out.println("Bowl(" + marker + ")");
    }
    void f1(int marker){
        System.out.println("f1(" + marker + ")");
    }
}
class Table{
    static Bowl bowl  = new Bowl(1);
    Table(){
        System.out.println("Table()");
        bowl2.f1(1);
    }
    void f2(int marker){
        System.out.println("f2(" + marker + ")");
    }
    static Bowl bowl2 = new Bowl(2);
}
class Cupboard{
    Bowl bowl3 = new Bowl(3);
    static Bowl bowl4 = new Bowl(4);
    Cupboard(){
        System.out.println("Cupboard()");
        bowl4.f1(2);
    }
    void f3(int marker){
        System.out.println("f3(" + marker + ")");
    }
    static Bowl bowl5 = new Bowl(5);
}
class StaticInitialization{
    static void f(){
        System.out.println("main creating new Cupboard()");
        new Cupboard();
        System.out.println("main creating new Cupboard()");
        new Cupboard();
        table.f2(1);
        cupboard.f3(1);
    }
    static Table table = new Table();
    static Cupboard cupboard = new Cupboard();
}


class Spoon{
    static int i ;
    static { // only run one once
        i = 47;
    }
}
class Cup{
    Cup(int marker){
        System.out.println("Cup(" + marker + ")");
    }
    void f(int marker){
        System.out.println("f(" + marker + ")");
    }
}
class Cups{
    static Cup cup1;
    static Cup cup2;
    static {
        cup1 = new Cup(1);
        cup2 = new Cup(2);
    }
    Cups(){
        System.out.println("Cups");
    }
}
class ExplicitStatic{
    static void f(){
        System.out.println("Inside main()");
        Cups.cup1.f(99); // [1]
    }
}


class Mug{
    Mug(int marker){
        System.out.println("Mug(" + marker + ")");
    }
}
class Mugs{
    Mug mug1 ;
    Mug mug2 ;
    {
        mug1 = new Mug(1);
        mug2 = new Mug(2);
        System.out.println("mug1 & mug2 initialized");
    }
    Mugs(){
        System.out.println("Mugs()");
    }
    Mugs(int i){
        System.out.println("Mug(int)");
    }
    static  void f(){
        System.out.println("inside main");
        new Mugs();
        System.out.println("new Mugs() completed");
        new Mugs(1);
        System.out.println("new Mugs(1) completed");
    }
}


class ArraysOfPrimitives{
    static void f(){
        int[] a1 = {1,2,3,4,5};
        int[] a2;
        a2 = a1;
        for (int i = 0 ;i < a2.length ; i++){
            a2[i] +=1;
        }
        for (int i = 0 ; i< a1.length ;i++){
            System.out.println("a1[" + i + "] = " + a1[i]);
        }
    }
}



class ArrayNew{
    static void f(){
        int[] a;
        Random rand = new Random(45);
        a = new int[rand.nextInt(20)];
        System.out.println("length of a = " + a.length);
        System.out.println(Arrays.toString(a));

    }
}


class ArrayClassObj{
    static void f(){
        Random rand = new Random(46);
        Integer[] a  = new Integer[rand.nextInt(20)];
        System.out.println("length of a = " + a.length);
        for (int i = 0 ; i < a.length ; i++){
            a[i] = rand.nextInt(500);
        }
        System.out.println(Arrays.toString(a));
    }

}



class ArrayInit{
    static void f(){
        Integer[] a ={
                1,2,3,
        };
        Integer[] b = new Integer[]{
                1,2,3,
        };
        System.out.println(Arrays.toString(a));
        System.out.println(Arrays.toString(b));
    }
}



class DynamicArray{
    static void f(){
        Other.f(new String[] {"fiddle","de","dem"});
    }
}
class Other{
    static  void f(String[] args){
        for (String s: args){
            System.out.println(s + " ");
        }
    }
}



class A{}
class VarArgs{
    static void printArray(Object[] args){
        for (Object obj : args){
            System.out.print(obj + " ");
        }
        System.out.println();
    }
    static void f(){
        printArray(new Object[] {47, (float) 3.14, 11.11});
        printArray(new Object[] {"one", "two", "three"});
        printArray(new Object[] {new A(), new A(), new A()});
    }
}


class NewVarArgs{
    static void printArray(Object... args){
        for (Object obj : args){
            System.out.print(obj + " ");
        }
        System.out.println();
    }
    static void f(){
        printArray(57,(float)3.14,11.11);
        printArray(47, 3.14F, 11.11);
        printArray("one", "two", "three");
        printArray(new A(), new A(), new A());
        // Or an array:
        printArray((Object[]) new Integer[] {1, 2, 3, 4});
        printArray(); // Empty list is OK
    }
}



class OptionalTrailingArguments{
    static void f(int required , String... trailing){
        System.out.print("required: " + required + " ");
        for (String s: trailing){
            System.out.print(s + " ");
        }
        System.out.println();
    }
    static void f(){
        f(1,"one");
        f(2, "two", "three");
        f(0);
    }
}



class VarargType{
    static void f(Character... args){
        System.out.print(args.getClass());
        System.out.println(" length " + args.length);
    }
    static void g(int... args){
        System.out.print(args.getClass());
        System.out.println(" length " + args.length);
    }
    static void s(){
        f('a');
        f();
        g(1);
        g();
        System.out.println("int[]: "+ new int[0].getClass());
    }
}


class AutoboxingVarargs{
    public static void f(Integer... args){
        for (Integer i: args){
            System.out.print(i + " ");
        }
        System.out.println();
    }
    static void f(){
        f(1,2);
        f(4, 5, 6, 7, 8, 9);
        f(10, 11, 12);
    }
}



class OverloadingVarargs {
    static void f(Character... args) {
        System.out.print("first");
        for (Character c : args) {
            System.out.print(" " + c);
        }
        System.out.println();
    }

    static void f(Integer... args) {
        System.out.print("second");
        for (Integer i : args) {
            System.out.print(" " + i);
        }
        System.out.println();
    }

    static void f(Long... args) {
        System.out.println("third");
    }

    static void s() {
        f('a', 'b', 'c');
        f(1);
        f(2, 1);
        f(0);
        f(0L);
        //- f(); // Won's compile -- ambiguous
    }
}



//class OverloadingVarargs2{
//    static void f(float i, Character... args){
//        System.out.println("first");
//    }
//    static void f(Character... args){
//        System.out.println("second");
//    }
//    static void s(){
//        f(1, 'a');
//        f('a', 'b');
//    }
//}



class OverloadingVarargs3{
    static void f(float i , Character... args){
        System.out.println("first");
    }
    static void f(char c ,Character... args){
        System.out.println("second");
    }
    static void s(){
        f(1, 'a');
        f('a', 'b');
    }
}




enum Spiciness{   // 枚举类型
    NOT, MILD, MEDIUM, HOT, FLAMING
}
class SimpleEnumUse{
    static void f(){
        Spiciness howHot = Spiciness.MEDIUM;
        System.out.println(howHot);
    }
}



class EnumOrder{
    static void f(){
        for (Spiciness s: Spiciness.values()){
            System.out.println(s + ", ordinal " + s.ordinal());
        }
    }
}



class Burrito{
    Spiciness degree;
    public Burrito(Spiciness degree){
        this.degree = degree;
    }
    public void describe(){
        System.out.print("This burrito is ");
        switch (degree){
            case NOT:
                System.out.println("not spicy at all.");
                break;
            case MILD:
            case MEDIUM:
                System.out.println("a little hot.");
                break;
            case HOT:
            case FLAMING:

                default:
                    System.out.println("maybe too hot");
        }
    }
    static void f(){
        Burrito plain = new Burrito(Spiciness.NOT),
                greenChile = new Burrito(Spiciness.MEDIUM),
                jalapeno = new Burrito(Spiciness.HOT);
        plain.describe();
        greenChile.describe();
        jalapeno.describe();
    }
}












public class Housekeep {
    public static void main(String[] args) {
//        SimpleConstructor.f();
//        Tree.f();
//        OverloadingOrder oo = new OverloadingOrder();
//        oo.t();
//        PrimitiveOverloading po = new PrimitiveOverloading();
//        po.f();
//        BananaPeel.f();
//        Leaf l = new Leaf();
//        l.f();
//        PassingThis pt = new PassingThis();
//        pt.f();
//        Flower f = new Flower();
//        f.f();
//        InitialValues.f();
//        Measurement m = new Measurement();
//        m.d.hashCode();
//        MethodInit2 mi = new MethodInit2();
//        int k = mi.j;
//        System.out.println(k);
//        OrderOfInitialization ooi = new OrderOfInitialization();
//        ooi.f();
//        StaticInitialization.f();
//        ExplicitStatic.f();
//        Mugs.f();
//        ArraysOfPrimitives.f();
//        ArrayNew.f();
//        ArrayClassObj.f();
//        ArrayInit.f();
//        DynamicArray.f();
//        VarArgs.f();
//        NewVarArgs.f();
//        OptionalTrailingArguments.f();
//        VarargType.s();
//        AutoboxingVarargs.f();
//        OverloadingVarargs.s();
//        OverloadingVarargs2.s();
//        OverloadingVarargs3.s();
//        SimpleEnumUse.f();
        EnumOrder.f();
        Burrito.f();
   }
}
