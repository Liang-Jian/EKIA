package thinkinjava8;


import java.util.Random;

/**
 *  8 charpter
 *  复用
 *
 *
 */



class WaterSource{
    private String s;
    WaterSource(){
        System.out.println("WaterSource()");
        s = "Constructed";
    }
    @Override
    public String toString(){
        return s ;
    }
}
class SprinklerSystem{
    private String valve1, valve2, valve3, valve4;
    private  WaterSource source = new WaterSource();
    private int i;
    private float f;
    @Override
    public String toString(){
        return
                "valve1 = " + valve1 + " " +
                "valve2 = " + valve2 + " " +
                "valve3 = " + valve3 + " " +
                "valve4 = " + valve4 + "\n" +
                "i = " + i + " " + "f = " + f + " " +
                "source = " + source; // [1]
    }
    static void f(){
        SprinklerSystem ss = new SprinklerSystem();
        System.out.println(ss);
    }
}



/*class Soap{
    private String s;
    Soap(){
        System.out.println("Soap()");
        s = "Constructed";
    }
    @Override
    public String toString(){
        return s;
    }
}
class Bath{
    private String s1 = "happy",
            s2 = "Happy",
            s3, s4;
    private Soap casille;
    private int i;
    private float toy;
    public Bath(){
        System.out.println("inside Bath()");
        s3 = "Joy";
    }
}*/




class Soap{
    private String s;
    Soap(){
        System.out.println("Soap");
        s = "Constructed";
    }
}
class Bath{
    private String s1 = "happy",
            s2 = "Happy",
            s3, s4;
    private Soap castille;
    private int i;
    private float toy;
    public Bath(){
        System.out.println("inside Bath()");
        s3 = "Joy";
        toy = 3.14f;
        castille = new Soap();
    }
    @Override
    public String toString(){
        if (s4 == null)
            s4 = "joy";
        return
                "s1 = " + s1 + "\n" +
                        "s2 = " + s2 + "\n" +
                        "s3 = " + s3 + "\n" +
                        "s4 = " + s4 + "\n" +
                        "i = " + i + "\n" +
                        "toy = " + toy + "\n" +
                        "castille = " + castille;
    }
    static void f(){
        Bath b = new Bath();
        System.out.println(b);
    }

}



class Cleanser{
    private String s = "Cleanser";
    public void append(String a ) { s += a; }
    public void dilute(){ append(" dilute()"); }
    public void apply() { append(" apply()"); }
    public void scrub() { append(" scrub()"); }

    @Override
    public String toString(){
        return s;
    }
    public static void f(){
        Cleanser x = new Cleanser();
        x.dilute(); x.apply(); x.scrub();
        System.out.println(x);
    }
}
class Detergent extends Cleanser{
    @Override
    public void scrub(){
        append(" Detergent.scrub()");
        super.scrub();
    }
    public void foam() { append(" foam()"); }
    public static void f(){
        Detergent x = new Detergent();
        x.dilute();
        x.apply();
        x.scrub();
        x.foam();
        System.out.println(x);
        System.out.println("Testing base class:");
        Cleanser.f();
    }
}



//无参调用
class Art{
    Art(){
        System.out.println("Art constructor");
    }
}
class  Drawing extends Art {
    Drawing(){
        System.out.println("Drawing constructor");
    }
}
class Cartoon extends Drawing {
    public Cartoon(){
        System.out.println("Cartoon constructor");
    }
    static void f(){
        Cartoon x = new Cartoon();
    }
}



// 参数调用
class Game{
    Game(int i ){
        System.out.println("Game constructor");
    }
}
class BoardGame extends Game{
    BoardGame(int i ){
        super(i);
        System.out.println("BoardGame constructor");
    }
}
class Chess extends BoardGame{
    Chess(){
        super(11);
        System.out.println("Chess constructor");
    }
    static void f(){
        Chess x = new Chess();
    }
}



// 委托
class SpaceShipControls{
    void up(int velocity) {}
    void down(int velocity) {}
    void left(int velocity) {}
    void right(int velocity) {}
    void forward(int velocity) {}
    void back(int velocity) {}
    void turboBoost() {}
}
class DerivedSpaceShip extends SpaceShipControls{
    private String name;
    public DerivedSpaceShip(String name){
        this.name = name;
    }
    @Override
    public String toString(){ return  name;}
    static void f(){
        DerivedSpaceShip protector = new DerivedSpaceShip("NASA Protector");
        protector.forward(100);
    }
}




class SpaceShipDelegation{
    private String name;
    private SpaceShipControls controls = new SpaceShipControls();
    public SpaceShipDelegation(String name){
        this.name = name;
    }
    public void back(int velocity){
        controls.back(velocity);
    }
    public void down(int velocity) {
        controls.down(velocity);
    }
    public void forward(int velocity) {
        controls.forward(velocity);
    }
    public void left(int velocity) {
        controls.left(velocity);
    }
    public void right(int velocity) {
        controls.right(velocity);
    }
    public void turboBoost() {
        controls.turboBoost();
    }
    public void up(int velocity) {
        controls.up(velocity);
    }
    static void f(){
        SpaceShipDelegation protector = new SpaceShipDelegation("NSEA Protector");
        protector.forward(100);
    }
}





// 结合组合和集成
class Plate{
    Plate(int i){
        System.out.println("Plate constructor");
    }
}
class DinnerPlate extends  Plate{
    DinnerPlate(int i){
        super(i);
        System.out.println("DinnerPlate constructor");
    }
}
class Utensil{
    Utensil(int i){
        System.out.println("Utensil constructor");
    }
}
class Spoon8 extends Utensil {  // 修改spoon -> spoon8 与housekeep 重复
    Spoon8(int i) {
        super(i);
        System.out.println("Spoon constructor");
    }
}
class Fork extends Utensil {
    Fork(int i) {
        super(i);
        System.out.println("Fork constructor");
    }
}
class Knife extends Utensil {
    Knife(int i) {
        super(i);
        System.out.println("Knife constructor");
    }
}
// A cultural way of doing something:
class Custom {
    Custom(int i) {
        System.out.println("Custom constructor");
    }
}
class PlaceSetting extends Custom{
    private Spoon8 sp;
    private Fork frk;
    private Knife kn;
    private DinnerPlate pl;
    public PlaceSetting(int i){
        super(i + 1);
        sp = new Spoon8(i + 2);
        frk = new Fork(i + 3);
        kn = new Knife(i + 4);
        pl = new DinnerPlate(i + 5);
        System.out.println("PlaceSetting constructor");
    }
    static void f(){
        PlaceSetting x = new PlaceSetting(9);
    }
}




class Shape{
    Shape(int i){
        System.out.println("Shape constructor");
    }
    void dispose(){
        System.out.println("Shape dispose");
    }
}
class Circle extends Shape{
    Circle(int i ){
        super(i);
        System.out.println("Drawing Circle");
    }
    @Override
    void dispose() {
        System.out.println("Erasing Circle");
        super.dispose();
    }
}
class Triangle extends Shape{
    Triangle(int i){
        super(i);
        System.out.println("Drawing Triangle");
    }
    @Override
    void dispose() {
        super.dispose();
        System.out.println("Erasing Triangle");
    }
}
class Line extends Shape{
    private int start,end;
    Line(int start , int end){
        super(start);
        this.start = start;
        this.end = end;
        System.out.println("Drawing Line: " + start + ", " + end);
    }
    @Override
    void dispose() {
        super.dispose();
//        System.out.println("Erasing Line: " + start + ", " + end);
    }
}
class CADSystem extends Shape{
    private Circle c;
    private Triangle t;
    private Line[] lines = new Line[3];
    CADSystem(int i){
        super(i);
        for(int j = 0; j < lines.length; j++)
            lines[j] = new Line(j, j*j);
        c = new Circle(1);
        t = new Triangle(1);
        System.out.println("Combined constructor");
    }
    @Override
    public void dispose(){
        System.out.println("CADSystem.dispose()");
        t.dispose();
        c.dispose();
        for(int i = lines.length - 1; i >= 0; i--)
            lines[i].dispose();
        super.dispose();
    }
    static void f(){
        CADSystem x = new CADSystem(47);
        try {
            ;
        }finally {
            x.dispose();
        }
    }

}





class Homer{
    char doh(char c){
        System.out.println("doh(char)");
        return 'd';
    }
    float doh(float f){
        System.out.println("doh(float)");
        return 1.0f;
    }
}
class Milhouse{}
class Bart extends Homer{
    void doh(Milhouse e){
        System.out.println("doh(Milhouse)");
    }
}
class Hide{
    static void f(){
        Bart b = new Bart();
        b.doh(1);
        b.doh('x');
        b.doh(1.0f);
        b.doh(new Milhouse());
    }
}



class Engine{
    public void start() {}
    public void rev() {}
    public void stop() {}
}
class Wheel{
    public void inflate(int psi) {}
}
class Window8{
    public void rollup() {}
    public void rolldown() {}
}
class Door {
    public Window8 window = new Window8();

    public void open() {}
    public void close() {}
}
class Car{
    public Engine engine = new Engine();
    public Wheel[] wheel = new Wheel[4];
    public Door left = new Door(), right = new Door(); // 2-door
    public Car(){
        for (int i = 0 ; i < 4 ; i++){
            wheel[i] = new Wheel();
        }
    }
    static void f(){
        Car car = new Car();
        car.left.window.rollup();
        car.wheel[0].inflate(72);
    }
}




// Protect  对外界隐藏，而允许派生类的成员访问。
class Villain{
    private String name;
    protected  void set(String nm){
        name =nm;
    }
    Villain(String name){
        this.name = name ;
    }
    @Override
    public String toString(){
        return "I'm a Villain and my name is " + name;
    }
}
class  Orc extends Villain{
    private int orcNumber;
    public Orc(String name,int orcNumber){
        super(name);
        this.orcNumber = orcNumber;
    }
    public void change(String name ,int orcNumber){
        set(name);
        this.orcNumber = orcNumber;
    }
    @Override
    public String toString(){
        return "Orc " + orcNumber + ": " + super.toString();
    }
    static void f(){
        Orc orc = new Orc("Limburger", 12);
        System.out.println(orc);
        orc.change("Bob", 19);
        System.out.println(orc);
    }
}




// 向上转型 新类是已有类的一种类型
class Instrument{
    public void play(){}
    static void tune(Instrument i){
        i.play();
    }
}
class Wind extends Instrument{
    static void f(){
        Wind flute = new Wind();
        Instrument.tune(flute);
    }
}




// final关键字
class Value8{
    int i;
    Value8(int i){
        this.i = i ;
    }
}
class FinalData{
    private static Random rand = new Random(47);
    private String id;
    public FinalData(String id){
        this.id = id;
    }
    private final int valueOne = 9;
    private static final int VALUE_TWO = 99;
    // Typical public constant:
    public static final int VALUE_THREE = 39;
    // Cannot be compile-time constants:
    private final int i4 = rand.nextInt(20);
    static final int INT_5 = rand.nextInt(20);
    private Value8 v1 = new Value8(11);
    private final Value8 v2 = new Value8(22);
    private static final Value8 VAL_3 = new Value8(33);
    // Arrays:
    private final int[] a = {1, 2, 3, 4, 5, 6};
    @Override
    public String toString(){
        return id + ": " + "i4 = " + i4 + ", INT_5 = " + INT_5;
    }
    static void f(){
        FinalData fd1 = new FinalData("fd1");
        //- fd1.valueOne++; // Error: can't change value
        fd1.v2.i++; // Object isn't constant
        fd1.v1 = new Value8(9); // OK -- not final
        for (int i = 0; i < fd1.a.length; i++) {
            fd1.a[i]++; // Object isn't constant
        }
        //- fd1.v2 = new Value(0); // Error: Can't
        //- fd1.VAL_3 = new Value(1); // change reference
        //- fd1.a = new int[3];
        System.out.println(fd1);
        System.out.println("Creating new FinalData");
        FinalData fd2 = new FinalData("fd2");
        System.out.println(fd1);
        System.out.println(fd2);
    }
}



// 空白 final
class Poppet{
    private int i;
    Poppet(int ii){
        i = ii;
    }
}
class BlankFinal{
    private final int i = 0;
    private final int j ;
    private final Poppet p;
    public BlankFinal(){
        j =1;
        p = new Poppet(1);
    }
    public BlankFinal(int x){
        j = x;
        p = new Poppet(x);
    }
    static void f(){
        new BlankFinal();
        new BlankFinal(45);
    }
}




//  final as 参数  主要用于传递数据给匿名内部类
class Gizmo{
    public void spin(){}
}
class FinalArguments{
    void with(final Gizmo g){}
    void without(Gizmo g){
        g = new Gizmo();
        g.spin();
    }
    int g(final int i){
        return  i + i;
    }
    static void f(){
        FinalArguments bf = new FinalArguments();
        bf.without(null);
        bf.with(null);
    }
}



// final 和 private
class WithFinals{
    private final void f(){
        System.out.println("WithFinals.f()");
    }
    private void g(){
        System.out.println("WithFinals.g()");
    }
}
class OverridingPrivate extends WithFinals{
    private final void f(){
        System.out.println("OverridingPrivate.f()");
    }
    private void g(){
        System.out.println("OverridingPrivate.g()");
    }
}
class OverridingPrivate2 extends OverridingPrivate{
    public final void f(){
        System.out.println("OverridingPrivate2.f()");;
    }
    public void g(){
        System.out.println("OverridingPrivate2.g()");
    }
}
class FinalOverridingIllusion{
    static void f(){
        OverridingPrivate2 op2 = new OverridingPrivate2();
        op2.f();
        op2.g();
        // You can upcast:
        OverridingPrivate op = op2;
        // But you can't call the methods:
        //- op.f();
        //- op.g();
        // Same here:
        WithFinals wf = op2;
        //- wf.f();
        //- wf.g();
    }
}




class SmallBrain{}
final class Dinosaur{
    int i = 7;
    int j = 1;
    SmallBrain x =new SmallBrain();
    void  f() {}
}
class Jurassic{
    static void f(){
        Dinosaur n = new Dinosaur();
        n.f();
        n.i = 40;
        n.j++;
    }
}



//  继承和初始化
class Insect{
    private int i = 9;
    protected int j;
    Insect(){
        System.out.println("i = " + i + ", j = " + j);
        j = 39;
    }
    private static int  x1 = printInit("static Insect.x1 initialized");
    static int printInit(String s) {
        System.out.println(s);
        return 47;
    }
}
class Beetle extends Insect{
    private int k = printInit("Beetle.k.initialized");
    public Beetle(){
        System.out.println("k = " + k);
        System.out.println("j = " + j);
    }
    private static int x2 = printInit("static Beetle.x2 initialized");
    static void f(){
        System.out.println("Beetle constructor");
        Beetle b = new Beetle();
    }
}












public class reuse {
    public static void main(String[] args) {
//        SprinklerSystem.f();
//        Bath.f();
//        Detergent.f();
//        Cartoon.f();
//        Chess.f();
//        DerivedSpaceShip.f();
//        SpaceShipDelegation.f();
//        PlaceSetting.f();
//        CADSystem.f();
//        Hide.f();
//        Car.f();
//        Orc.f();
//        Wind.f();
//        FinalData.f();
//        BlankFinal.f();
//        FinalOverridingIllusion.f();
//        Jurassic.f();
        Beetle.f();
    }
}
