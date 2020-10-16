package thinkinjava8;


import java.util.Random;

/**
 *
 *  9 chapter
 *  多 态
 *
 */




enum Note{ // meiju type
    MIDDLE_C, C_SHARP, B_FLAT; // Etc.
}
class Instrument9{
    public void play(Note n){
        System.out.println("Instrument.play()");
    }
}
class Wind9 extends Instrument9{
    @Override
    public void play(Note n){
        System.out.println("Wind.play() " + n);
    }
}
class Music{
    public static void tune(Instrument9 i){
        i.play(Note.MIDDLE_C);
    }
    static void f(){
        Wind9 flute = new Wind9();
        tune(flute);
    }
}



// 向上转型
class Stringed extends  Instrument9{
    @Override
    public void play(Note n){
        System.out.println("Stringed.play() " + n);
    }
}
class Brass extends  Instrument9{
    @Override
    public void play(Note n){
        System.out.println("Brass.play() " + n);
    }
}
class Music2{
    public static void tune(Wind9 i){
        i.play(Note.MIDDLE_C);
    }
    public static void tune(Stringed i){
        i.play(Note.MIDDLE_C);
    }
    public static void tune(Brass i){
        i.play(Note.MIDDLE_C);
    }
    static void f(){
        Wind9 flute = new Wind9();
        Stringed violin = new Stringed();
        Brass frenchHorn = new Brass();
        tune(flute); // No upcasting
        tune(violin);
        tune(frenchHorn);
    }
}



// 产生正确的行为
class Shape9{
    public void draw() {}
    public void erase() {}
}
class Circle9 extends Shape9{
    @Override
    public void draw(){
        System.out.println("Circle.draw()");
    }
    @Override
    public void erase(){
        System.out.println("Circle.erase()");
    }
}
class Square extends Shape9{
    @Override
    public void draw(){
        System.out.println("Square.draw()");
    }
    @Override
    public void erase() {
        System.out.println("Square.erase()");
    }
}
class Triangle9 extends Shape9{
    @Override
    public void draw() {
        System.out.println("Triangle.draw()");
    }
    @Override
    public void erase() {
        System.out.println("Triangle.erase()");
    }
}
class RandomShapes{
    private Random rand = new Random(45);
    public  Shape9 get(){
        switch(rand.nextInt(3)) {
            default:
            case 0: return new Circle9();
            case 1: return new Square();
            case 2: return new Triangle9();
        }
    }
    public Shape9[] array(int sz) {
        Shape9[] shapes = new Shape9[sz];
        // Fill up the array with shapes:
        for (int i = 0; i < shapes.length; i++) {
            shapes[i] = get();
        }
        return shapes;
    }
}
class Shapes{
    static void f(){
        RandomShapes gen = new RandomShapes();
        for (Shape9 shape: gen.array(9)){
            shape.draw();
        }
    }
}




// 可扩展性
class Instrument99{
    void play(Note n){
        System.out.println("Instrument.play() " + n);
    }
    void adjust(){
        System.out.println("Adjusting Instrument");
    }
    String what(){
        return "Instrument";
    }
}
class Wind99 extends Instrument99{
    @Override
    void play(Note n) {
        System.out.println("Wind.play() " + n);
    }
    @Override
    String what(){
        return "wind99";
    }
    @Override
    void adjust(){
        System.out.println("Adjusting Wind");
    }
}
class Percussion extends  Instrument99{
    @Override
    public void play(Note n) {
        System.out.println("Percussion.play() " + n);
    }
    @Override
    String what(){
        return "Percussion";
    }
    @Override
    void adjust(){
        System.out.println("Adjusting Percussion");
    }
}
class Stringed99 extends Instrument99{
    @Override
    void play(Note n) {
        System.out.println("Stringed.play() " + n);
    }
    @Override
    String what() {
        return "Stringed";
    }
    @Override
    void adjust() {
        System.out.println("Adjusting Stringed");
    }
}
class Brass99 extends Instrument99 {
    @Override
    void play(Note n) {
        System.out.println("Brass.play() " + n);
    }
    @Override
    void adjust() {
        System.out.println("Adjusting Brass");
    }
}
class Woodwind extends Wind99 {
    @Override
    void play(Note n) {
        System.out.println("Woodwind.play() " + n);
    }
    @Override
    String what() {
        return "Woodwind";
    }
}
class Music3{
    public static void tune(Instrument99 i){
        i.play(Note.MIDDLE_C);
    }
    public static void tuneAll(Instrument99[] e){
        for (Instrument99 i: e) {
            tune(i);
        }
    }
    static void f(){
        Instrument99[] orchestra = {
                new Wind99(),
                new Percussion(),
                new Stringed99(),
                new Brass99(),
                new Woodwind()
        };
        tuneAll(orchestra);
    }
}




// error demo : 错误: 方法不会覆盖或实现超类型的方法
/*class PrivateOverride2 {
    private void f() {
        System.out.println("private f()");
    }

    public static void main(String[] args) {
        PrivateOverride2 po = new Derived2();
        po.f();
    }
}
class Derived2 extends PrivateOverride2 {
    @Override
    public void f() {
        System.out.println("public f()");
    }
}*/



// 属性与静态方法
class Super{
    public int field = 0;
    public int getField(){
        return field;
    }
}
class Sub extends Super{
    public  int field = 1;
    @Override
    public int getField(){
        return field;
    }
    public int getSuperField(){
        return super.field;
    }
}
class FieldAccess{
    static void f(){
        Super sup = new Sub(); // Upcast
        System.out.println("sup.field = " + sup.field +
                ", sup.getField() = " + sup.getField());
        Sub sub = new Sub();
        System.out.println("sub.field = " + sub.field +
                ", sub.getField() = " + sub.getField()
                + ", sub.getSuperField() = " + sub.getSuperField());
    }
}



// 静态的方法只与类关联，与单个的对象无关。
//一个方法是静态static的，它的行为就不具有多态性：
class StaticSuper{
    public static String staticGet(){
        return "Base staticGet()";
    }
    public String dynamicGet(){
        return "Base dynamicGet()";
    }
}
class StaticSub extends StaticSuper{
    public static String staticGet(){
        return "Derived staticGet()";
    }
    @Override
    public String dynamicGet(){
        return "Derived dynamicGet()";
    }
}
class StaticPolymorphism{
    static void f(){
        StaticSuper sup = new StaticSub(); // Upcast
        System.out.println(StaticSuper.staticGet());
        System.out.println(sup.dynamicGet());
    }
}



// 构造器和多态
// 组合、继承和多态在构建顺序上的作用：
class Meal{
    Meal(){
        System.out.println("Meal()");
    }
}
class Bread{
    Bread(){
        System.out.println("Bread()");
    }
}
class Cheese{
    Cheese(){
        System.out.println("Cheese()");
    }
}
class Lettuce{
    Lettuce(){
        System.out.println("Lettuce()");
    }
}
class Lunch9 extends  Meal{
    Lunch9(){
        System.out.println("Lunch()");
    }
}
class PortableLunch extends Lunch9{
    PortableLunch() {
        System.out.println("PortableLunch()");
    }
}
class Sandwich extends PortableLunch{
    private Bread b = new Bread();
    private Cheese c = new Cheese();
    private Lettuce l = new Lettuce();
    public Sandwich(){
        System.out.println("Sandwich()");
    }
    static void f(){
        new Sandwich();
    }
}




class Characteristic{
    private String s;
    Characteristic(String s){
        this.s = s;
        System.out.println("Creating Characteristic " + s);
    }
    protected void dispose(){
        System.out.println("disposing Characteristic " + s);
    }
}
class Description{
    private String s;
    Description(String s){
        this.s = s ;
        System.out.println("Creating Description " + s);
    }
    protected void dispose(){
        System.out.println("disposing Description " + s);
    }
}
class LivingCreature{
    private Characteristic p = new Characteristic("is alive");
    private Description t = new Description("Basic Living Creature");
    LivingCreature(){
        System.out.println("LivingCreature()");
    }
    protected void dispose(){
        System.out.println("LivingCreature dispose");
        t.dispose();
        p.dispose();
    }
}
class Animal extends LivingCreature{
    private Characteristic p = new Characteristic("has heart");
    private Description t = new Description("Animal not Vegetable");
    Animal() {
        System.out.println("Animal()");
    }
    @Override
    protected void dispose() {
        System.out.println("Animal dispose");
        t.dispose();
        p.dispose();
        super.dispose();
    }
}
class Amphibian extends Animal {
    private Characteristic p = new Characteristic("can live in water");
    private Description t = new Description("Both water and land");

    Amphibian() {
        System.out.println("Amphibian()");
    }

    @Override
    protected void dispose() {
        System.out.println("Amphibian dispose");
        t.dispose();
        p.dispose();
        super.dispose();
    }
}
class Frog extends Amphibian{
    private Characteristic p = new Characteristic("Croaks");
    private Description t = new Description("Eats Bugs");
    public Frog(){
        System.out.println("Frog()");
    }
    @Override
    protected void dispose() {
        System.out.println("Frog dispose");
        t.dispose();
        p.dispose();
        super.dispose();
    }
    static void f(){
        Frog frog = new Frog();
        System.out.println("Bye!");
        frog.dispose();
    }
}





class Shared{
    private int refcount = 0 ;
    private static long counter =0;
    private  final long id = counter++;

    Shared(){
        System.out.println("Creating " + this);
    }
    public void addRef(){
        refcount++;
    }
    protected void dispose(){
        if (--refcount ==  0 ){
            System.out.println("Disposing " + this);
        }
    }
    @Override
    public String toString(){
        return  "Shared " + id;
    }
}
class Composing{
    private Shared shared;
    private static long counter = 0;
    private final long id = counter++;
    Composing(Shared shared){
        System.out.println("Creating " + this);
        this.shared = shared;
        this.shared.addRef();
    }
    protected void dispose() {
        System.out.println("disposing " + this);
        shared.dispose();
    }

    @Override
    public String toString() {
        return "Composing " + id;
    }
}
class ReferenceCounting{
    static void f(){
        Shared shared = new Shared();
        Composing[] composing = {
                new Composing(shared),
                new Composing(shared),
                new Composing(shared),
                new Composing(shared),
                new Composing(shared),
        };
        for (Composing c: composing) {
            c.dispose();
        }
    }
}




class Glyph{
    void draw(){
        System.out.println("Glyph.draw()");
    }
    Glyph(){
        System.out.println("Glyph() before draw()");
        draw();
        System.out.println("Glyph() after  draw()");
    }
}
class RoundGlyph extends Glyph{
    private int radius = 1;
    RoundGlyph(int r){
        radius =r ;
        System.out.println("RoundGlyph.RoundGlyph(), radius = " + radius);
    }
    @Override
    void draw(){
        System.out.println("RoundGlyph.draw(), radius = " + radius);
    }
}
class PolyConstructors{
    static void f(){
        new RoundGlyph(5);
    }
}




class Grain{
    @Override
    public String toString(){
        return "Grain";
    }
}
class  Wheat extends Grain {
    @Override
    public String toString() {
        return "Wheat";
    }
}
class Mill{
    Grain process(){
        return new Grain();
    }
}
class WheatMill extends Mill {
    @Override
    Wheat process() {
        return new Wheat();
    }
}
class CovariantReturn{
    static void f(){
        Mill m = new Mill();
        Grain g = m.process();
        System.out.println(g);
        m = new WheatMill();
        g = m.process();
        System.out.println(g);
    }
}



//使用继承设计


class Actor{
    public void act() {}
}
class  HappyActor extends Actor{
    @Override
    public void act() {
        System.out.println("HappyActor");
    }
}
class  SadActor extends Actor {
    @Override
    public void act() {
        System.out.println("SadActor");
    }
}
class Stage{
    private Actor actor = new HappyActor();
    public void change() {
        actor = new SadActor();
    }
    public void performPlay() {
        actor.act();
    }
}
class Transmogrify{
    static void f(){
        Stage stage = new Stage();
        stage.performPlay();
        stage.change();
        stage.performPlay();
    }
}


// error demo
class Useful{
    public void f(){}
    public void g(){}
}
class  MoreUseful extends Useful {
    @Override
    public void f() {}
    @Override
    public void g() {}
    public void u() {}
    public void v() {}
    public void w() {}
}
class RTTI{
    static void f(){
        Useful[] x = {
                new Useful(),
                new MoreUseful()
        };
        x[0].f();
        x[1].g();
        // Compile time: method not found in Useful:
        //- x[1].u();
        ((MoreUseful) x[1]).u(); // Downcast/RTTI
        ((MoreUseful) x[0]).u(); // Exception thrown
    }
}









public class Polymorphism {
    public static void main(String[] args) {
//        Music.f();
//        Music2.f();
//        Shapes.f();
//        Music3.f();
//        FieldAccess.f();
//        StaticPolymorphism.f();
//        Sandwich.f();
//        Frog.f();
//        ReferenceCounting.f();
//        PolyConstructors.f();
//        CovariantReturn.f();
//        Transmogrify.f();
        RTTI.f();
    }
}
