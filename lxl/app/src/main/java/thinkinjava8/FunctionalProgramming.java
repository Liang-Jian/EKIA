package thinkinjava8;


import java.util.function.Function;

/**
 *  13 ｃｈａｐｔｅｒ
 *　函数式编程
 */


//**Strategy** 接口提供了单一的 `approach()` 方法来承载函数式功能。通过创建不同的 **Strategy** 对象，我们可以创建不同的行为。
//
//我们一般通过创建一个实现**Strategy**接口的类来实现这种行为，正如在**Soft**里所做的。
interface Strategy{
    String approach(String msg);
}
class Soft implements Strategy {
    public String approach(String msg) {
        return msg.toLowerCase() + "?";
    }
}
class Unrelated {
    static String twice(String msg) {
        return msg + " " + msg;
    }
}
class Strategize {
    Strategy strategy;
    String msg;
    Strategize(String msg) {
        strategy = new Soft(); // [1]
        this.msg = msg;
    }
    void communicate() {
        System.out.println(strategy.approach(msg));
    }

    void changeStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    static void f() {
        Strategy[] strategies = {
                new Strategy() { // [2]
                    public String approach(String msg) {
                        return msg.toUpperCase() + "!";
                    }
                },
                msg -> msg.substring(0, 5), // [3]
                Unrelated::twice // [4]
        };
        Strategize s = new Strategize("Hello there");
        s.communicate();
        for(Strategy newStrategy : strategies) {
            s.changeStrategy(newStrategy); // [5]
            s.communicate(); // [6]
        }
    }
}



//Lambda表达式
//我们从三个接口开始，每个接口都有一个单独的方法（很快就会理解它的重要性）。但是，每个方法都有不同数量的参数，以便演示 Lambda 表达式语法。
interface Description13 {
    String brief();
}
interface Body {
    String detailed(String head);
}
interface Multi {
    String twoArg(String head, Double d);
}
class LambdaExpressions {
    static Body bod = h -> h + " No Parens!"; // [1]

    static Body bod2 = (h) -> h + " More details"; // [2]

    static Description13 desc = () -> "Short info"; // [3]

    static Multi mult = (h, n) -> h + n; // [4]

    static Description13 moreLines = () -> { // [5]
        System.out.println("moreLines()");
        return "from moreLines()";
    };

    static void f() {
        System.out.println(bod.detailed("Oh!"));
        System.out.println(bod2.detailed("Hi!"));
        System.out.println(desc.brief());
        System.out.println(mult.twoArg("Pi! ", 3.14159));
        System.out.println(moreLines.brief());
    }
}


//### 递归
//
//递归函数是一个自我调用的函数。可以编写递归的 Lambda 表达式，但需要注意：递归方法必须是实例变量或静态变量，否则会出现编译时错误。 我们将为每个案例创建一个示例。
interface IntCall {
    int call(int arg);
}
class RecursiveFactorial {
    static IntCall fact;
    static void f() {
        fact = n -> n == 0 ? 1 : n * fact.call(n - 1);
        for(int i = 0; i <= 10; i++)
            System.out.println(fact.call(i));
    }
}




class RecursiveFibonacci{
    IntCall fib;

    RecursiveFibonacci() {
        fib = n -> n == 0 ? 0 :
                n == 1 ? 1 :
                        fib.call(n - 1) + fib.call(n - 2);
    }
    int fibonacci(int n) { return fib.call(n); }
    static void f() {
        RecursiveFibonacci rf = new RecursiveFibonacci();
        for(int i = 0; i <= 10; i++)
            System.out.println(rf.fibonacci(i));
    }
}




// 方法引用
interface Callable { // [1]
    void call(String s);
}
class Describe {
    void show(String msg) { // [2]
        System.out.println(msg);
    }
}
class MethodReferences {
    static void hello(String name) { // [3]
        System.out.println("Hello, " + name);
    }
    static class Description {
        String about;
        Description(String desc) { about = desc; }
        void help(String msg) { // [4]
            System.out.println(about + " " + msg);
        }
    }
    static class Helper {
        static void assist(String msg) { // [5]
            System.out.println(msg);
        }
    }
    static void f() {
        Describe d = new Describe();
        Callable c = d::show; // [6]
        c.call("call()"); // [7]

        c = MethodReferences::hello; // [8]
        c.call("Bob");

        c = new Description("valuable")::help; // [9]
        c.call("information");

        c = Helper::assist; // [10]
        c.call("Help!");
    }
}



// Runnable接口
class Go {
    static void go() {
        System.out.println("Go::go()");
    }
}
class RunnableMethodReference {
    static void f() {
        new Thread(new Runnable() {
            public void run() {
                System.out.println("Anonymous");
            }
        }).start();

        new Thread(
                () -> System.out.println("lambda")
        ).start();

        new Thread(Go::go).start();
    }
}



// 未绑定的方法引用是指没有关联对象的普通（非静态）方法。 使用未绑定的引用时，我们必须先提供对象：
class X {
    String f() { return "X::f()"; }
}
interface MakeString {
    String make();
}
interface TransformX {
    String transform(X x);
}
class UnboundMethodReference {
    static void f() {
        // MakeString ms = X::f; // [1]
        TransformX sp = X::f;
        X x = new X();
        System.out.println(sp.transform(x)); // [2]
        System.out.println(x.f()); // 同等效果
    }
}




//
class This {
    void two(int i, double d) {}
    void three(int i, double d, String s) {}
    void four(int i, double d, String s, char c) {}
}
interface TwoArgs {
    void call2(This athis, int i, double d);
}
interface ThreeArgs {
    void call3(This athis, int i, double d, String s);
}
interface FourArgs {
    void call4(
            This athis, int i, double d, String s, char c);
}
class MultiUnbound {
    static void f() {
        TwoArgs twoargs = This::two;
        ThreeArgs threeargs = This::three;
        FourArgs fourargs = This::four;
        This athis = new This();
        twoargs.call2(athis, 11, 3.14);
        threeargs.call3(athis, 11, 3.14, "Three");
        fourargs.call4(athis, 11, 3.14, "Four", 'Z');
    }
}





// `X :: f` 表示未绑定的方法引用，因为它尚未“绑定”到对象。
class Dog {
    String name;
    int age = -1; // For "unknown"
    Dog() { name = "stray"; }
    Dog(String nm) { name = nm; }
    Dog(String nm, int yrs) { name = nm; age = yrs; }
}
interface MakeNoArgs {
    Dog make();
}
interface Make1Arg {
    Dog make(String nm);
}
interface Make2Args {
    Dog make(String nm, int age);
}
class CtorReference {
    static void f() {
        MakeNoArgs mna = Dog::new; // [1]
        Make1Arg m1a = Dog::new;   // [2]
        Make2Args m2a = Dog::new;  // [3]

        Dog dn = mna.make();
        Dog d1 = m1a.make("Comet");
        Dog d2 = m2a.make("Ralph", 4);
    }
}




//在编写接口时，可以使用 `@FunctionalInterface` 注解强制执行此“函数式方法”模式：
@FunctionalInterface
interface Functional {
    String goodbye(String arg);
}
interface FunctionalNoAnn {
    String goodbye(String arg);
}
/*
@FunctionalInterface
interface NotFunctional {
  String goodbye(String arg);
  String hello(String arg);
}
产生错误信息:
NotFunctional is not a functional interface
multiple non-overriding abstract methods
found in interface NotFunctional
*/
class FunctionalAnnotation {
    public String goodbye(String arg) {
        return "Goodbye, " + arg;
    }
    static void f() {
        FunctionalAnnotation fa =
                new FunctionalAnnotation();
        Functional f = fa::goodbye;
        FunctionalNoAnn fna = fa::goodbye;
        // Functional fac = fa; // Incompatible
        Functional fl = a -> "Goodbye, " + a;
        FunctionalNoAnn fnal = a -> "Goodbye, " + a;
    }
}




/*
//import java.util.function.*;

class Foo {}

class Bar {
    Foo f;
    Bar(Foo f) { this.f = f; }
}

class IBaz {
    int i;
    IBaz(int i) {
        this.i = i;
    }
}

class LBaz {
    long l;
    LBaz(long l) {
        this.l = l;
    }
}

class DBaz {
    double d;
    DBaz(double d) {
        this.d = d;
    }
}

public class FunctionVariants {
    static Function<Foo,Bar> f1 = f -> new Bar(f);
    static IntFunction<IBaz> f2 = i -> new IBaz(i);
    static LongFunction<LBaz> f3 = l -> new LBaz(l);
    static DoubleFunction<DBaz> f4 = d -> new DBaz(d);
    static ToIntFunction<IBaz> f5 = ib -> ib.i;
    static ToLongFunction<LBaz> f6 = lb -> lb.l;
    static ToDoubleFunction<DBaz> f7 = db -> db.d;
    static IntToLongFunction f8 = i -> i;
    static IntToDoubleFunction f9 = i -> i;
    static LongToIntFunction f10 = l -> (int)l;
    static LongToDoubleFunction f11 = l -> l;
    static DoubleToIntFunction f12 = d -> (int)d;
    static DoubleToLongFunction f13 = d -> (long)d;

    public static void main(String[] args) {
        Bar b = f1.apply(new Foo());
        IBaz ib = f2.apply(11);
        LBaz lb = f3.apply(11);
        DBaz db = f4.apply(11);
        int i = f5.applyAsInt(ib);
        long l = f6.applyAsLong(lb);
        double d = f7.applyAsDouble(db);
        l = f8.applyAsLong(12);
        d = f9.applyAsDouble(12);
        i = f10.applyAsInt(12);
        d = f11.applyAsDouble(12);
        i = f12.applyAsInt(13.0);
        l = f13.applyAsLong(13.0);
    }
}*/




//高阶函数
interface FuncSS extends Function<String, String> {} // [1]

class ProduceFunction {
    static FuncSS produce() {
        return s -> s.toLowerCase(); // [2]
    }
    public static void main(String[] args) {
        FuncSS f = produce();
        System.out.println(f.apply("YELLING"));
    }
}





public class FunctionalProgramming {
    public static void main(String[] args) {
//        Strategize.f();
//        LambdaExpressions.f();
//        RecursiveFactorial.f();
//        RecursiveFibonacci.f();
//        MethodReferences.f();
//        RunnableMethodReference.f();
//        UnboundMethodReference.f();
//        MultiUnbound.f();
//        CtorReference.f();
        FunctionalAnnotation.f();
    }
}
