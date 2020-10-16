package thinkinjava8;


import java.util.Arrays;
import java.nio.*;
import java.util.*;

/**
 *
 *  10 chapter
 *  接口
 *
 */



// java 不会创建抽象类的对象
abstract class Basic{
    abstract void unimplemented();
}


abstract class Basic2 extends Basic{
    int f(){
        return 111;
    }
    abstract void g();
}
abstract class Basic3{
    int f(){
        return 111;
    }
}
class AbstractWithoutAbstracts{}




abstract class Uninstantiable{
    abstract void f();
    abstract int g();
}
class Instantiable extends Uninstantiable{
    @Override
    void f(){
        System.out.println("f()");
    }
    @Override
    int g(){
        return 22;
    }
    static void ff(){
        Uninstantiable ui = new Instantiable();
    }
}





abstract class AbstractAccess {
    private void m1() {}
    // private abstract void m1a(); // illegal
    protected void m2() {}
    protected abstract void m2a();
    void m3() {}
    abstract void m3a();
    public void m4() {}
    public abstract void m4a();
}








abstract class Instrument10 {
    private int i; // Storage allocated for each

    public abstract void play(Note n);

    public String what() {
        return "Instrument";
    }

    public abstract void adjust();
}
class Wind10 extends Instrument10 {
    @Override
    public void play(Note n) {
        System.out.println("Wind.play() " + n);
    }

    @Override
    public String what() {
        return "Wind";
    }

    @Override
    public void adjust() {
        System.out.println("Adjusting Wind");
    }
}
class Percussion10 extends Instrument10 {
    @Override
    public void play(Note n) {
        System.out.println("Percussion.play() " + n);
    }

    @Override
    public String what() {
        return "Percussion";
    }

    @Override
    public void adjust() {
        System.out.println("Adjusting Percussion");
    }
}
class Stringed10 extends Instrument10 {
    @Override
    public void play(Note n) {
        System.out.println("Stringed.play() " + n);
    }
    @Override
    public String what() {
        return "Stringed";
    }
    @Override
    public void adjust() {
        System.out.println("Adjusting Stringed");
    }
}
class Brass10 extends Wind10 {
    @Override
    public void play(Note n) {
        System.out.println("Brass.play() " + n);
    }

    @Override
    public void adjust() {
        System.out.println("Adjusting Brass");
    }
}
class Woodwind10 extends Wind10 {
    @Override
    public void play(Note n) {
        System.out.println("Woodwind.play() " + n);
    }

    @Override
    public String what() {
        return "Woodwind";
    }
}
class Music4 {
    // Doesn't care about type, so new types
    // added to system still work right:
    static void tune(Instrument10 i) {
        // ...
        i.play(Note.MIDDLE_C);
    }
    static void tuneAll(Instrument10[] e) {
        for (Instrument10 i: e) {
            tune(i);
        }
    }
    static void f() {
        // Upcasting during addition to the array:
        Instrument10[] orchestra = {
                new Wind10(),
                new Percussion10(),
                new Stringed10(),
                new Brass10(),
                new Woodwind10()
        };
        tuneAll(orchestra);
    }
}





interface Concept{
    void idea1();
    void idea2();
}
class Implementation implements Concept {
    @Override
    public void idea1() {
        System.out.println("idea1");
    }

    @Override
    public void idea2() {
        System.out.println("idea2");
    }
}




// 默认方法default 为 `newMethod()` 方法提供默认的实现，那么所有与接口有关的代码能正常工作，不受影响，而且这些代码还可以调用新的方法 `newMethod()
interface AnInterface {
    void firstMethod();
    void secondMethod();
}
class AnImplementation implements AnInterface {
    public void firstMethod() {
        System.out.println("firstMethod");
    }

    public void secondMethod() {
        System.out.println("secondMethod");
    }

    static void f() {
        AnInterface i = new AnImplementation();
        i.firstMethod();
        i.secondMethod();
    }
}





interface InterfaceWithDefault{
    void firstMethod();
    void secondMethod();

    default void newMethod(){
        System.out.println("newMethod");
    }
}
class Implementation2 implements InterfaceWithDefault {
    @Override
    public void firstMethod() {
        System.out.println("firstMethod");
    }

    @Override
    public void secondMethod() {
        System.out.println("secondMethod");
    }

    static void f() {
        InterfaceWithDefault i = new Implementation2();
        i.firstMethod();
        i.secondMethod();
        i.newMethod();
    }
}





interface One{
    default void first() {
        System.out.println("first");
    }
}
interface Two{
    default void second() {
        System.out.println("second");
    }
}
interface Three{
    default void third() {
        System.out.println("third");
    }
}
class MI implements One, Two, Three {}
class MultipleInheritance{
    static void f(){
        MI mi = new MI();
        mi.first();
        mi.second();
        mi.third();
    }
}





interface Bob1{
    default void bob(){
        System.out.println("Bob1::bob");
    }
}
interface Bob2{
    default void bob() {
        System.out.println("Bob2::bob");
    }
}
interface Sam1 {
    default void sam() {
        System.out.println("Sam1::sam");
    }
}
interface Sam2 {
    default void sam(int i) {
        System.out.println(i * 2);
    }
}
class Sam implements Sam1,Sam2{}
interface Max1 {
    default void max() {
        System.out.println("Max1::max");
    }
}
interface Max2 {
    default int max() {
        return 47;
    }
}
interface Jim1 {
    default void jim() {
        System.out.println("Jim1::jim");
    }
}
interface Jim2 {
    default void jim() {
        System.out.println("Jim2::jim");
    }
}
class Jim implements Jim1, Jim2 {
    @Override
    public void jim() {
        Jim2.super.jim();
    }

    static void f() {
        new Jim().jim();
    }
}




interface Operations{
    void execute();
    static void runOps(Operations... ops){
        for (Operations op: ops) {
            op.execute();
        }
    }
    static void show(String msg){
        System.out.println(msg);
    }
}
class Bing implements Operations{
    @Override
    public void execute() {
        Operations.show("Bings");
    }
}
class Crack implements Operations{
    @Override
    public void execute() {
        Operations.show("Crack");
    }
}
class Twist implements Operations{
    @Override
    public void execute() {
        Operations.show("Twist");
    }
}
class Machine{
    static void f(){
        Operations.runOps(new Bing(),new Crack(),new Twist());
    }
}




interface Instrument100{
    int VALUE = 5; //
    default void play(Note n){
        System.out.println(this + ".play() " + n);
    }
    default void adjust(){
        System.out.println("Adjusting " + this);
    }
}
class Wind100 implements Instrument100 {
    @Override
    public String toString() {
        return "Wind";
    }
}
class Percussion100 implements Instrument100 {
    @Override
    public String toString() {
        return "Percussion";
    }
}
class Stringed100 implements Instrument100 {
    @Override
    public String toString() {
        return "Stringed";
    }
}
class Brass100 extends Wind100 {
    @Override
    public String toString() {
        return "Brass";
    }
}
class Woodwind100 extends Wind100 {
    @Override
    public String toString() {
        return "Woodwind";
    }
}
class Music5{
    static void tune(Instrument100 i) {
        // ...
        i.play(Note.MIDDLE_C);
    }

    static void tuneAll(Instrument100[] e) {
        for (Instrument100 i: e) {
            tune(i);
        }
    }
    static void f(){
        Instrument100[] orchestra = {
                new Wind100(),
                new Percussion100(),
                new Stringed100(),
                new Brass100(),
                new Woodwind100()
        };
        tuneAll(orchestra);

    }
}






/*


抽象类和接口的区别
        -----------------------------------------------------------------------------------------------------------------------------
        |         特性         |                            接口                            |                  抽象类                  |
        | :------------------: | :--------------------------------------------------------: | :--------------------------------------: |
        |         组合         |                    新类可以组合多个接口                    |            只能继承单一抽象类            |
        |         状态         |        不能包含属性（除了静态属性，不支持对象状态）        | 可以包含属性，非抽象方法可能引用这些属性 |
        | 默认方法 和 抽象方法 | 不需要在子类中实现默认方法。默认方法可以引用其他接口的方法 |         必须在子类中实现抽象方法         |
        |        构造器        |                         没有构造器                         |               可以有构造器               |
        |        可见性        |                      隐式 **public**                       |       可以是 **protected** 或友元        |
         ---------------------------------------------------------------------------------------------------------------------------


抽象类仍然是一个类，在创建新类时只能继承它一个。而创建类的过程中可以实现多个接口。


*/

class Processor{
    public String name(){
        return getClass().getSimpleName();
    }
    public Object process(Object input) {
        return input;
    }
}
class Upcase extends Processor {
    // 返回协变类型
    @Override
    public String process(Object input) {
        return ((String) input).toUpperCase();
    }
}
class Downcase extends Processor {
    @Override
    public String process(Object input) {
        return ((String) input).toLowerCase();
    }
}
class Splitter extends Processor {
    @Override
    public String process(Object input) {
        // split() divides a String into pieces:
        return Arrays.toString(((String) input).split(" "));
    }
}
class Applicator{
    public static void apply(Processor p, Object s) {
        System.out.println("Using Processor " + p.name());
        System.out.println(p.process(s));
    }
    public static void f(){
        String s = "We are such stuff as dreams are made on";
        apply(new Upcase(), s);
        apply(new Downcase(), s);
        apply(new Splitter(), s);
    }
}




class Waveform{
    private static long counter;
    private final long id = counter++;

    @Override
    public String toString() {
        return "Waveform " + id;
    }
}
class Filter {
    public String name() {
        return getClass().getSimpleName();
    }
    public Waveform process(Waveform input) {
        return input;
    }
}
class LowPass extends Filter {
    double cutoff;

    public LowPass(double cutoff) {
        this.cutoff = cutoff;
    }
    @Override
    public Waveform process(Waveform input) {
        return input; // Dummy processing 哑处理
    }
}
class HighPass extends Filter {
    double cutoff;

    public HighPass(double cutoff) {
        this.cutoff = cutoff;
    }
    @Override
    public Waveform process(Waveform input) {
        return input;
    }
}
class BandPass extends Filter {
    double lowCutoff, highCutoff;

    public BandPass(double lowCut, double highCut) {
        lowCutoff = lowCut;
        highCutoff = highCut;
    }
    @Override
    public Waveform process(Waveform input) {
        return input;
    }
}





interface Processor1 {
    default String name() {
        return getClass().getSimpleName();
    }

    Object process(Object input);
}
class Applicator1 {
    public static void apply(Processor1 p, Object s) {
        System.out.println("Using Processor " + p.name());
        System.out.println(p.process(s));
    }
}




//复用代码的第一种方式是客户端程序员遵循接口编写类，像这样：
interface StringProcessor extends Processor1 {
    @Override
    String process(Object input); // [1]
    String S = "If she weighs the same as a duck, she's made of wood"; // [2]

    static void f() { // [3]
        Applicator1.apply(new Upcase1(), S);
        Applicator1.apply(new Downcase1(), S);
        Applicator1.apply(new Splitter1(), S);
    }
}
class Upcase1 implements StringProcessor {
    // 返回协变类型
    @Override
    public String process(Object input) {
        return ((String) input).toUpperCase();
    }
}
class Downcase1 implements StringProcessor {
    @Override
    public String process(Object input) {
        return ((String) input).toLowerCase();
    }
}
class Splitter1 implements StringProcessor {
    @Override
    public String process(Object input) {
        return Arrays.toString(((String) input).split(" "));
    }
}




//*适配器*设计模式。适配器允许代码接受已有的接口产生需要的接口
class FilterAdapter implements Processor1 {
    Filter filter;

    FilterAdapter(Filter filter) {
        this.filter = filter;
    }

    @Override
    public String name() {
        return filter.name();
    }

    @Override
    public Waveform process(Object input) {
        return filter.process((Waveform) input);
    }
}
class FilterProcessor{
    static void f(){
        Waveform w = new Waveform();
        Applicator1.apply(new FilterAdapter(new LowPass(1.0)), w);
        Applicator1.apply(new FilterAdapter(new HighPass(2.0)), w);
        Applicator1.apply(new FilterAdapter(new BandPass(3.0, 4.0)), w);
    }
}




/* 派生类并不要求必须继承自抽象的或“具体的”（没有任何抽象方法）的基类。如果继承一个非接口的类，那么只能继承一个类，
*  其余的基元素必须都是接口。需要将所有的接口名称置于 **implements** 关键字之后且用逗号分隔。可以有任意多个接口，
*  并可以向上转型为每个接口，因为每个接口都是独立的类型。下例展示了一个由多个接口组合而成的具体类产生的新类：
 */
interface CanFight {
    void fight();
}
interface CanSwim {
    void swim();
}
interface CanFly {
    void fly();
}
class ActionCharacter {
    public void fight(){}
}
class Hero extends ActionCharacter implements CanFight, CanSwim, CanFly {
    public void swim() {}
    public void fly() {}
}
class Adventure{
    public static void t(CanFight x) {
        x.fight();
    }

    public static void u(CanSwim x) {
        x.swim();
    }

    public static void v(CanFly x) {
        x.fly();
    }

    public static void w(ActionCharacter x) {
        x.fight();
    }
    static void f() {
        Hero h = new Hero();
        t(h); // Treat it as a CanFight
        u(h); // Treat it as a CanSwim
        v(h); // Treat it as a CanFly
        w(h); // Treat it as an ActionCharacter
    }
}





//使用继承扩展接口,**extends** 只能用于单一类，但是在构建接口时可以引用多个基类接口。注意到，接口名之间用逗号分隔。
interface Monster {
    void menace();
}
interface DangerousMonster extends Monster {
    void destroy();
}
interface Lethal {
    void kill();
}
class DragonZilla implements DangerousMonster {
    @Override
    public void menace() {}
    @Override
    public void destroy() {}
}
interface Vampire extends DangerousMonster, Lethal {
    void drinkBlood();
}
class VeryBadVampire implements Vampire {
    @Override
    public void menace() {}
    @Override
    public void destroy() {}
    @Override
    public void kill() {}
    @Override
    public void drinkBlood() {}
}
class HorrorShow{
    static void u(Monster b) {
        b.menace();
    }
    static void v(DangerousMonster d) {
        d.menace();
        d.destroy();
    }

    static void w(Lethal l) {
        l.kill();
    }
    static void f(){
        DangerousMonster barney = new DragonZilla();
        u(barney);
        v(barney);
        Vampire vlad = new VeryBadVampire();
        u(vlad);
        v(vlad);
        w(vlad);
    }
}





class RandomStrings implements Readable {
    private static Random rand = new Random(47);
    private static final char[] CAPITALS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();
    private static final char[] LOWERS = "abcdefghijklmnopqrstuvwxyz".toCharArray();
    private static final char[] VOWELS = "aeiou".toCharArray();
    private int count;

    public RandomStrings(int count) {
        this.count = count;
    }

    @Override
    public int read(CharBuffer cb) {
        if (count-- == 0) {
            return -1; // indicates end of input
        }
        cb.append(CAPITALS[rand.nextInt(CAPITALS.length)]);
        for (int i = 0; i < 4; i++) {
            cb.append(VOWELS[rand.nextInt(VOWELS.length)]);
            cb.append(LOWERS[rand.nextInt(LOWERS.length)]);
        }
        cb.append(" ");
        return 10; // Number of characters appended
    }

    static void f() {
        Scanner s = new Scanner(new RandomStrings(10));
        while (s.hasNext()) {
            System.out.println(s.next());
        }
    }
}




//假设你有一个类没有实现 **Readable** 接口，怎样才能让 **Scanner** 作用于它呢
interface RandomDoubles {
    Random RAND = new Random(47);

    default double next() {
        return RAND.nextDouble();
    }

    static void f() {
        RandomDoubles rd = new RandomDoubles(){};
        for (int i = 0; i < 7; i++) {
            System.out.println(rd.next() + " ");
        }
    }
}





//意味着一个接受接口类型的方法提供了一种让任何类都可以与该方法进行适配的方式。这就是使用接口而不是类的强大之处。
class AdaptedRandomDoubles implements RandomDoubles, Readable {
    private int count;

    public AdaptedRandomDoubles(int count) {
        this.count = count;
    }

    @Override
    public int read(CharBuffer cb) {
        if (count-- == 0) {
            return -1;
        }
        String result = Double.toString(next()) + " ";
        cb.append(result);
        return result.length();
    }

    static void f() {
        Scanner s = new Scanner(new AdaptedRandomDoubles(7));
        while (s.hasNextDouble()) {
            System.out.print(s.nextDouble() + " ");
        }
    }
}





//初始化接口中的字段
interface RandVals{
    Random RAND = new Random(47);
    int RANDOM_INT = RAND.nextInt(10);
    long RANDOM_LONG = RAND.nextLong() * 10;
    float RANDOM_FLOAT = RAND.nextLong() * 10;
    double RANDOM_DOUBLE = RAND.nextDouble() * 10;
}
class TestRandVals{
    static void f(){
        System.out.println(RandVals.RANDOM_INT);
        System.out.println(RandVals.RANDOM_LONG);
        System.out.println(RandVals.RANDOM_FLOAT);
        System.out.println(RandVals.RANDOM_DOUBLE);
    }
}




//接口嵌套,接口可以嵌套在类或其他接口中

class A1 {
    interface B {
        void f();
    }

    public class BImp implements B {
        @Override
        public void f() {}
    }

    public class BImp2 implements B {
        @Override
        public void f() {}
    }

    public interface C {
        void f();
    }

    class CImp implements C {
        @Override
        public void f() {}
    }

    private class CImp2 implements C {
        @Override
        public void f() {}
    }

    private interface D {
        void f();
    }

    private class DImp implements D {
        @Override
        public void f() {}
    }

    public class DImp2 implements D {
        @Override
        public void f() {}
    }

    public D getD() {
        return new DImp2();
    }

    private D dRef;

    public void receiveD(D d) {
        dRef = d;
        dRef.f();
    }
}

interface E {
    interface G {
        void f();
    }
    // Redundant "public"
    public interface H {
        void f();
    }

    void g();
    // Cannot be private within an interface
    //- private interface I {}
}

class NestingInterfaces {
    public class BImp implements A1.B {
        @Override
        public void f() {}
    }

    class CImp implements A1.C {
        @Override
        public void f() {}
    }
    // Cannot implements a private interface except
    // within that interface's defining class:
    //- class DImp implements A.D {
    //- public void f() {}
    //- }
    class EImp implements E {
        @Override
        public void g() {}
    }

    class EGImp implements E.G {
        @Override
        public void f() {}
    }

    class EImp2 implements E {
        @Override
        public void g() {}

        class EG implements E.G {
            @Override
            public void f() {}
        }
    }

    static void f() {
        A1 a = new A1();
        // Can't access to A.D:
        //- A.D ad = a.getD();
        // Doesn't return anything but A.D:
        //- A.DImp2 di2 = a.getD();
        // cannot access a member of the interface:
        //- a.getD().f();
        // Only another A can do anything with getD():
        A1 a2 = new A1();
        a2.receiveD(a.getD());
    }
}




//接口是多实现的途径，而生成符合某个接口的对象的典型方式是*工厂方法*设计模式
interface Service {
    void method1();
    void method2();
}
interface ServiceFactory {
    Service getService();
}
class Service1 implements Service {
    Service1() {} // Package access

    @Override
    public void method1() {
        System.out.println("Service1 method1");
    }

    @Override
    public void method2() {
        System.out.println("Service1 method2");
    }
}
class Service1Factory implements ServiceFactory {
    @Override
    public Service getService() {
        return new Service1();
    }
}
class Service2 implements Service {
    Service2() {} // Package access

    @Override
    public void method1() {
        System.out.println("Service2 method1");
    }

    @Override
    public void method2() {
        System.out.println("Service2 method2");
    }
}
class Service2Factory implements ServiceFactory {
    @Override
    public Service getService() {
        return new Service2();
    }
}
class Factories {
    public static void serviceConsumer(ServiceFactory fact) {
        Service s = fact.getService();
        s.method1();
        s.method2();
    }

    static void f() {
        serviceConsumer(new Service1Factory());
        // Services are completely interchangeable:
        serviceConsumer(new Service2Factory());
    }
}


/**
 * 任何抽象性都应该是由真正的需求驱动的。当有必要时才应该使用接口进行重构，
 * 而不是到处添加额外的间接层，从而带来额外的复杂性。这种复杂性非常显著，
 * 如果你让某人去处理这种复杂性，只是因为你意识到“以防万一”而添加新接口，而没有其他具有说服力的原因
 */
interface Game1 {
    boolean move();
}
interface GameFactory {
    Game1 getGame();
}
class Checkers implements Game1 {
    private int moves = 0;
    private static final int MOVES = 3;

    @Override
    public boolean move() {
        System.out.println("Checkers move " + moves);
        return ++moves != MOVES;
    }
}
class CheckersFactory implements GameFactory {
    @Override
    public Game1 getGame() {
        return new Checkers();
    }
}
class Chess1 implements Game1 {
    private int moves = 0;
    private static final int MOVES = 4;

    @Override
    public boolean move() {
        System.out.println("Chess move " + moves);
        return ++moves != MOVES;
    }
}
class ChessFactory implements GameFactory {
    @Override
    public Game1 getGame() {
        return new Chess1();
    }
}
class Games {
    public static void playGame(GameFactory factory) {
        Game1 s = factory.getGame();
        while (s.move()) {
            ;
        }
    }
    static void f() {
        playGame(new CheckersFactory());
        playGame(new ChessFactory());
    }
}






public class interfaces {
    public static void main(String[] args) {
//        Instantiable.ff();
//        Music4.f();
//        AnImplementation.f();
//        Implementation2.f();
//        MultipleInheritance.f();
//        Jim.f();
//        Machine.f();
//        Music5.f();
//        Applicator.f();

//        StringProcessor.f();
//        FilterProcessor.f();
//        Adventure.f();
//        HorrorShow.f();
//        RandomStrings.f();
//        RandomDoubles.f();
//        AdaptedRandomDoubles.f();
//        TestRandVals.f();
//        NestingInterfaces.f();
//        Factories.f();
        Games.f();
    }

}
