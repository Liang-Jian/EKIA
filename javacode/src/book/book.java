package book;

import java.util.Date;
import java.util.Random;


class ShowPro{
    //p31 获取运行系统所有的属性
    void f(){
        System.getProperties().list(System.out);
        System.out.println(System.getProperty("user.name"));
        System.out.println(System.getProperty("java.library.path"));
    }
    void hellodate(){
        System.out.println(new Date());;
    }
}


class OverFlow{
    //P63
    void f(){
        int big = Integer.MAX_VALUE;
        System.out.println("big:"+ big);
        int bigger = big * 4;
        System.out.println("bigger:"+ bigger);
    }
}

class WhileTest{
    //P64 get random int
    static boolean condition(){
        boolean result = Math.random() < 0.99;
        System.out.println("result ?" + result);
        return result;
    }
    void f(){
        while (condition()){
            System.out.println("inside 'while'");
        }
        System.out.println("Exited 'while'");
    }
}
class ListChar{
    //p66
    void f(){
        for (char c = 0 ; c < 128 ; c++)
            if (Character.isLowerCase(c)) {
                System.out.println("value:" + new Integer(c) + ", character:" + c );
            }
    }
}
class CommaOperator{ //p67
    void  f(){
        for (int i = 0 , j = i+ 10;  i < 5; i++,j = i *2){
            System.out.println("i:" + i + "j:"+j);
        }
    }
}
class ForEachMethod{ //p67 new for method
    void f(){
        Random random = new Random(45);
        float f[] = new float[10];
        for (int i = 0 ; i < 10 ; i++)
            f[i] = random.nextFloat();
        for (float x : f)
            System.out.println(x);
    }
}
class ForeachString{//p68
    void r(){
        for (char c :"An arfrican swllow".toCharArray())
            System.out.println(c+ "");
    }
}
class ForeachInt{
    //p68 error
    void r(){
//        for (int i: range(10))
//            System.out.println("i"+i);
    }
}
class IfElse{//p69 if else
    int f(int start , int end){
        if (start >  end)
            return +1;
        else if (start< end)
            return -1;
        else
            return 0;
    }
}
class BreakACon{
    //p70
    void f(){
        for (int i=0 ; i < 100; i++){
            if (i == 77) break;
            if (i % 9 != 0) continue;
            System.out.print(i);
        }
        System.out.println();
        int i = 0 ;
        while (true){
            i++;
            int j = i * 23;
            if (j == 1259) break;
            if (j % 10 != 0) continue;
            System.out.println(i + "");
        }
    }
}
class VowelAndCon{
    //p74 switch case method
    void f(){
        Random rand = new Random(49);
        for (int i = 0; i< 100; i++){
            int c = rand.nextInt(23) + 'a'; // get lower zimu..*_).
            System.out.print(new Character((char) c));
            switch (c){
                case 'a':
                case 'e':
                case 'i':
                case 'o':
                case 'u':
                    System.out.println("aeiod");
                    break;
                    default:
                        System.out.println("constant");
            }
        }
    }
}
class Rock{
    //p77
    Rock(){
        System.out.println("Rock");
    }
}
class SimpleCon{
    void f(){
        for (int i = 0 ; i< 10 ;i++)
            new Rock();
    }
}
class Rock2{
    //p77
    Rock2(int i){
        System.out.println("Rock2:" + i);
    }
}
class Simplecon{
    void f(){
        for (int i = 0; i < 8 ;i++)
            new Rock2(i);
    }
}
class Tree{//78
    int height;
    Tree(){
        System.out.println("plant a tree");
        height = 0;

    }
    Tree(int initi){
        height = initi;
        System.out.println("Create new Tree that is "+ height + " feet tail");
    }
    void info(){
        System.out.println("Tree is "+ height + "feet tall");
    }
    void info(String s ){
        System.out.println(s+":Tree is " + height + "f eet tall");
    }
}
class OverLoading{
    void f(){
        for (int i = 0 ; i< 5 ; i++){
            Tree t = new Tree(i);
            t.info();;
            t.info("over loading method");
        }
        new Tree();
    }
}

class Bird{//p83
    Bird(int i){}
    Bird(String s){}
}
class Nosy{
    Bird bd = new Bird("s");
    Bird bd1 = new Bird(23);
//    Bird bd2 = new Bird(); // error if defind goutzaoqi .no defautl get
}

class Leaf{ //p85 this return current object used .
    int i = 0 ;
    Leaf incread(){
        i++;
        return this;
    }
    void printf(){
        System.out.println("i="+i);
    }
    void f(){
        Leaf x= new Leaf();
        x.incread().incread().incread().printf();
    }
}

class Person{ //85 current object tranmato other method used
    void eat(Apple apple){
        Apple peeled = apple.getPeeled();
        System.out.println("yummy");
    }
}
class Peeler{
    static Apple pell(Apple apple){
        return apple;
    }
}
class Apple{
    Apple getPeeled() { return Peeler.pell(this);}
}
class PassingThis{
    void f(){
        new Person().eat(new Apple());
    }
}

class Flower{
    int petalCount = 0 ;
    String s = "init value";
    Flower(int petals){
        petalCount  = petals;
        System.out.println("contru w/ int args only,petalcont＝" + petalCount);
    }
    Flower(String ss){
        System.out.println("contru w/ String arg only" + ss);
        s = ss;
    }
    Flower(String s, int petals){
        this(petals);
        this.s = s ;
        System.out.println("string && integer");
    }
    Flower(){
        this("hi",34);
        System.out.println("defautl construment (no) args");
    }
    void printPealcount(){
        System.out.println("petalcount" + petalCount + " s = " + s );
    }

    void f(){
        Flower x = new Flower();
        x.printPealcount();
    }
}

class InitialValues3{//p93
    boolean bool = false;
    char ch = 'x';
    byte b = 34;
    int i = 990;
    short s = 0xff;
    long lng = 1;
    float f = 3.15f;
    double d = 3.13143;
}
class Depth{}
class Measurment{ Depth d  = new Depth();} //非基本类型的初始化

class MethodInit{ //p93
    int i = f() ;
    int f(){ return 11;}
}
class MethodInit2{
    int i = f();
    int j = g(i);
    int f() { return  11;}
    int g(int n) { return  n * 10;}
}
class MethodInit3{
//    int j = g(i); 只有初始化后才可以使用.error
    int i = f();
    int f() { return  11;}
    int g(int n) { return  n * 99;}
}

class Counter{ //97
    int i;
    Counter(){ i = 7;}
}

class Bowl{//95
    Bowl(int marker){
        System.out.println("Bowl");
    }
    void f1(int marker){
        System.out.println("f1(" + marker + ")");
    }
}
class Table{
    static Bowl bowl =  new Bowl(1);
    Table(){
        System.out.println("table()");
        bowl2.f1(1);
    }
    void f2(int marker){
        System.out.println("f2(" + marker +")");
    }
    static Bowl bowl2 = new Bowl(2);
}
class CupBoard{
    Bowl bowl3 = new Bowl(3);
    static Bowl bowl4 = new Bowl(4);
    CupBoard(){
        System.out.println("cupboard");
        bowl4.f1(2);
    }
    void f3(int marker){
        System.out.println("f3(" + marker + ")");
    }
    static Bowl bowl5 = new Bowl(5);
}
class StaticInit{ //96
    void f(){
        System.out.println("creating new cupboard() in main");
        new CupBoard();
        System.out.println("creating new cupboard() in main");
        new CupBoard();
        table.f2(1);
        cupBoard.f3(1);
    }
    static Table table  = new Table();
    static CupBoard cupBoard = new CupBoard();
}

class Cup{ //97
    Cup(int marker){
        System.out.println("Cup("+ marker + ")");
    }
    void f(int marker){
        System.out.println("f(" + marker + ")");
    }
}
class Cups{
    static Cup cup1 ;
    static Cup cup2 ;
    static {
        cup1 = new Cup(1);
        cup2 = new Cup(2);
    }
    Cups(){
        System.out.println("Cups()");
    }
}
class ExplicitStatic{
    void f(){
        System.out.println("inside Main()");
        Cups.cup1.f(99);
    }
}

class Mug{
    //P98 静态方法的使用,不用static 关键字也可以..实例化子句是在初始化两个构造器之间执行的
    public Mug(int marker) {
        System.out.println("Mug("+ marker+")");
    }
    void f (int marker){
        System.out.println("f("+ marker +")");
    }
}
class Mugs {
    Mug mug1;
    Mug mug2;{
        mug1 = new Mug(1);
        mug1 = new Mug(2);
        System.out.println("mug1 & mug2 initialized");
    }
    Mugs() {
        System.out.println("Mugs()");
    }
    Mugs(int i ){
        System.out.println("Mugs(int)");
    }
    void f() {
        System.out.println("inside main");
        new Mugs();
        System.out.println("new Mugs() completed");
        new Mugs(1);
        System.out.println("new Mug(int) completed");
    }
}

class ArayOfPri{ //99
    void f(){
        int[] a1 = {1,2,3,4,5,6};
        int[] a2 ;
        a2 = a1;
        for (int i = 0 ; i < a2.length ; i++)
            a2[i] = a2[i] + 1;
        for (int i = 0 ; i < a2.length ; i++)
            System.out.println("a2[" + i + "]=" + a1[i]);
    }
}
class NewArgs{//102
    static void printArray(Object[]...args){
        for (Object obj: args){
            System.out.println(obj + " ");
        }
        System.out.println();
    }
    void f(){
//        printArray(new Integer(34),new Float(3.43),new Double(11.11));
//        printArray(45,3.14f,11.11);
//        printArray("one","two","three");
        printArray((Object[])new  Integer[]{1,2,3,4});
        printArray();
    }
}

class OptionalTrai{ //102
    static void f(int required ,String... trai){
        System.out.print("required: "+ required + " ");
        for (String s:trai)
            System.out.print(s+ " ");
        System.out.println();
    }
    void f(){
        f(1,"one");
        f(2,"two","three");
        f(0);
    }
}

class VarargType{ //103
    static  void f(Character ... args){
        System.out.println(args.getClass());
        System.out.println("length" + args.length);
    }
    static void g(int ...args){
        System.out.println(args.getClass());
        System.out.println("lenght" + args.length);
    }
    void f(){
        f('a');
//        f();
        g(1);
        g();
        System.out.println("int[]" + new int[0].getClass());
    }
}

class AutoBoxing{ //kebian canshu he zidong baozhuangjizhi
    static void f(int... args){
        for (Integer i : args)
            System.out.print(i + " ");
        System.out.println();
    }
    void f(){
        f(new Integer(1),new Integer(2));
        f(4,5,6,7,8,9);
        f(10,new Integer(11),22);
    }
}

class OverloadingVarargs{ //104
    static  void f(Character ...args){
        System.out.println("first");
        for (Character c: args)
            System.out.print(" "+c);
        System.out.println();
    }
    static  void f(Integer ...args){
        System.out.print("second");
        for (Integer i : args)
            System.out.print(" "+ i);
        System.out.println();
    }
    static  void f(Long ... args){
        System.out.print("Third");
    }
}
class OverloadingVarargs2{ // 105
    static  void f (float i ,Character... args){
        System.out.println("first");
    }
    //使用错误
    static  void f(char c ,Character... args){
        System.out.println("second");
    }
    void f(){
        f(1,'a');
        f('a','b');
    }
}
enum Spiciness{
    NOT,MILD,MEDIUM,HOT,FLAMING
}
class SimpleEnumCase{ //106
    void f(){
        Spiciness sp = Spiciness.MEDIUM;
        System.out.println(sp);
    }
}

class EnumOrder{ //106 for enum case
    void f(){
        for (Spiciness s : Spiciness.values())
            System.out.println(s + " orderal " + s.ordinal());
    }
}
class Burrito{ //106
    Spiciness degree;
    public Burrito(Spiciness degree){
        this.degree = degree;
    }

    void describe(){
        System.out.println("this burrito is ");
        switch (degree){
            case NOT:
                System.out.print("not spicy at all");break;
            case  MILD:
            case MEDIUM:
                System.out.print("a little hot.");break;
            case HOT:
            case FLAMING:
                default:
                    System.out.println("maybe too hot.");
        }
    }
    void f(){
        Burrito plain = new Burrito(Spiciness.NOT),
                greenChild = new Burrito(Spiciness.MEDIUM),
                jalaeno = new Burrito(Spiciness.HOT);
        plain.describe();
        greenChild.describe();
        jalaeno.describe();
    }
}

class Sundae{ //118 defense other get class
    private Sundae(){}
    static Sundae makesundae(){
        return new Sundae();
    }
}
class IceCream{
//    Sundae x = new Sundae();
    Sundae y = Sundae.makesundae();
}

class Soup1{ //119
    private Soup1(){}
    public static Soup1 makesoup(){
        return new Soup1();
    }
}
class Soup2{
    private Soup2() {}
    private  static Soup2 ps1 = new Soup2();
    public   static Soup2 access() {
        return ps1;
    }
    public void f(){}
}
class Lunch{
    void testPrivate(){

    }
    void testStatic(){
        Soup1 soup = Soup1.makesoup();
    }
    void testSing(){
        Soup2.access().f();
    }
}
class WaterSource {//P125 服用类
    private String s;
    WaterSource() {
        System.out.println("WaterSource()");
        s = "contstructer";
    }
    public String toString() {
        return s;
    }
}
class SprinklerSystem {
    private String valve1,valve2,valve3,valve4;
    private WaterSource source = new WaterSource();
    private int i ;
    private float f;
    public String toString() {
        return
                "valve1:="+valve1+"\n"+
                        "valve2:="+valve2+"\n"+
                        "valve3:="+valve3+"\n"+
                        "valve4:="+valve4+"\n"+
                        "i ="+ i +
                        "f:= "+f+
                        "source=" + source;
    }
    void f() {
        SprinklerSystem sprink = new SprinklerSystem();
        System.out.println(sprink);
    }
}
class	Soap {
    //126
    private	String	s;
    Soap()	{
        System.out.println("Soap()");
        s	=	new	String("Constructed");
    }
    public	String	toString()	{	return	s;	}
}
class	Bath {
    private	String
            s1	=	new	String("Happy"),
            s2	=	"Happy",
            s3,	s4;
    private Soap castille;
    private int	i;
    private float toy;
    public Bath()	{
        System.out.println("Inside	Bath()");
        s3	=	new	String("Joy");
        toy	=	3.14f;
        castille	=	new	Soap();
    }
    public String toString(){
        if (s4 == null){
            s4 ="joy";
        }
        return
                "s1 =" +s1+"\n"+
                        "s2 =" +s2+"\n"+
                        "s3 =" +s3+"\n"+
                        "s4 ="+ s4+"\n"+
                        "i="+ i +"\n"+
                        "toy= " +toy+"\n"+
                        "castille =" +castille;
    }
    void f(){
        Bath	b	=	new	Bath();
        System.out.println(b);
    }
}

class	Cleanser {
    //127	继承method
    private	String	s	=	new	String("Cleanser");
    public	void	append(String	a)	{
        s	+=	a;
    }
    public	void	dilute(){
        append("dilute()");
    }
    public	void	apply(){
        append("apply()");
    }
    public	void	scrub(){
        append("scrub()");
    }
    public	void	print(){
        System.out.println(s);
    }
    public	static	void	main(String[]	args)	{
        Cleanser	x	=	new	Cleanser();
        x.dilute();	x.apply();	x.scrub();
        x.print();
    }   //Cleanser	dilute()	apply()	scrub()
}
class	Detergent	extends	Cleanser {
    public	void	scrub()	{
        append(" Detergent.scrub()");
        super.scrub();	//	call base class
    }
    public	void	foam()	{	append(" foam()");	}
    void f(String[] args){
        Detergent	x	=	new	Detergent();
        x.dilute();
        x.apply();
        x.scrub();
        x.foam();
        x.print();
        System.out.println("Testing	base	class:");
        Cleanser.main(args);
    }
}
class Art {// 129定义3 个类，Art ,Drw , Cart ，分别继承输出
    Art() {
        System.out.println("Art");
    }
}
class Drw extends Art {
    Drw() {
        System.out.println("Drw");
    }
}
class Cartoon extends Drw {
    Cartoon() {
        System.out.println("Cartoon");
    }
    void f() {
        Cartoon s = new Cartoon();
    }
}

class Game {// 130 如果不调用BoardGames()内的基础类构建器，编译器就会报告自己找不到Games()形式的一个构建器。
    Game(int i) {
        System.out.println("Game constructor");
    }
}
class BoardGame extends Game {
    BoardGame(int i) {
        super(i);
        System.out.println("BoardGame constructor");
    }
}
class Chess extends BoardGame {
    Chess(int i) {
        super(13);
        System.out.println("Chess constructor");
    }
    void f() {
        Chess x = new Chess(5);
    }
}

class SpaceShipControls {//131代理
    void up(int velocity){};
    void down(int velocity){};
    void left(int velocity){};
    void right(int velocity){};
    void forward(int velocity){};
    void back(int velocity){};
    void turboBoost(){};
}
class SpaceShip extends SpaceShipControls{
    private String name;
    public SpaceShip(String name) {this.name = name;}
    public String toString() {return name;}
//    private SpaceShipControls control = new SpaceShipControls();
    void f(){
        SpaceShip sp = new SpaceShip("NASA Protector");
        sp.forward(11);
    }

//    public void up(int velocity){
//        control.back(velocity);
//    }
//    protected static void sct() {
//        SpaceShip sp = new SpaceShip("NSA");
//        sp.up(32);
//    }
}

class SpaceShipDelegation { //131 代理模式，内部使用private class name
    private String name;
    private  SpaceShipControls controls = new SpaceShipControls();
    public SpaceShipDelegation(String name) {this.name = name;}
    public void back(int velocity) { controls.back(velocity);}
    public void down(int velocity) { controls.down(velocity);}
    public void forward(int velocity)  {controls.forward(velocity);}
    public void left(int velocity) {controls.left(velocity);}
    public void right(int velocity) {controls.right(velocity);}
    public void turboboost() {controls.turboBoost();}
    public void up(int velocity) {controls.up(velocity);}
    void f() {
        SpaceShipDelegation proterctor = new SpaceShipDelegation("NSEA Protector");
        proterctor.forward(100);
    }
}


class Plate {
    //P132 组合和继承结合使用
    Plate(int i)
    {
        System.out.println("Plate constructor");
    }
}
class DinnerPlate extends Plate {
    DinnerPlate(int i)
    {
        super(i);
        System.out.println("DinnerPlate constructor");
    }
}
class Utensil {
    Utensil(int i)
    {
        System.out.println("Utensil constructor");
    }
}
class Spoon extends Utensil {
    Spoon(int i)
    {
        super(i);
        System.out.println("Spoon constructor");
    }
}
class Fork extends Utensil {
    Fork(int i)
    {
        super(i);
        System.out.println("Fork constructor");
    }
}
class Knife extends Utensil {
    Knife(int i)
    {
        super(i);
        System.out.println("Knife constructor");
    }
}

//A cultural way of doing something:
class Custom {
    Custom(int i)
    {
        System.out.println("Custom constructor");
    }
}
class PlaceSetting extends Custom {
    private Spoon sp;
    private Fork frk;
    private Knife kn;
    private DinnerPlate pl;
    public PlaceSetting(int i) {
        super(i + 1);
        sp = new Spoon(i + 2);
        frk = new Fork(i + 3);
        kn = new Knife(i + 4);
        pl = new DinnerPlate(i + 5);
        System.out.println("PlaceSetting constructor");
    }
    protected static void f() {
        PlaceSetting x = new PlaceSetting(9);
    }
}

class Homer {
    //136 
    char doh(char c) {
        System.out.println("doh(char)");
        return 'd';
    }
    float doh(float f) {
        System.out.println("doh(float)");
        return 1.0f;
    }
}
class Milhouse{}
class Bart extends Homer{
    void doh(Milhouse m){
        System.out.println("doh(Milhouse)");
    }
}

class Hide {
    protected static void sct(String[] args){
        Bart b = new Bart();
        b.doh(1);
        b.doh('x');
        b.doh(1.0f);
        b.doh(new Milhouse());
    }
}

class Engine{ //137
    public void start(){};
    public void rev(){};
    public void stop(){}
}
class Wheel{
    public void infalte(int psi){}
}
class Windows{
    public  void rollup(){}
    public  void rolldown(){}
}
class Door{
    public Windows windows = new Windows();
    public void open() {}
    public void close() {}
}
class Car{
    public Engine engine = new Engine();
    public Wheel[] wheels  = new Wheel[4];
    public Door left = new Door(),right = new Door();
    public Car(){
        for (int i = 0 ; i < 4 ;i++)
            wheels[i] = new Wheel();
    }
    void f(){
        Car car = new Car();
        car.left.windows.rollup();;
        car.wheels[0].infalte(72);
    }
}

class Villain{
    //138change可以访问set(),这是因为他是protected
    private String name;
    protected void set (String nm){name = nm;}
    public Villain(String name) {this.name = name;}
    public String toString() {
        return "i'm avillain and my name is "+ name;
    }
}
class Orc extends Villain{
    private int orcNumber;
    public Orc(String name , int orcNumber){
        super(name);
        this.orcNumber = orcNumber;
    }
    public void change(String name ,int orcNumber){
        set(name);
        this.orcNumber = orcNumber;
    }
    public String toString(){
        return "Orc" + orcNumber + ":" + super.toString();
    }
    protected static void sct(){
        Orc orc = new Orc("limburger" , 12);
        System.out.println(orc);
        orc.change("bob", 19);
        System.out.println(orc);
    }
}

class Instrument{ //139 xiang shang zhuangxing ..
    public void play(){
        System.out.println("Instrument().play");
    }
    static void tune(Instrument i) {
        i.play();
    }
}
class Wind extends  Instrument{
    void f(){
        Wind flute = new Wind();
        Instrument.tune(flute);
    }
}

class Value { //140  final
    int i = 1;
    public Value(int i ){ this.i = i;}
}
class FinalData {
    private static Random rand	= new Random(47);
    private String id;
    public FinalData (String id ){this.id = id;}
    private final int valueOne  = 9;
    private static final int VALUE_two = 99;
    public static final int VALUE_THREE = 39;
    private final int i4 = rand.nextInt(20);
    static final int INT_5 = rand.nextInt(20);
    private Value v1 = new Value(11);
    private final Value v2 = new Value(22);
    private final Value VAL_3 = new Value(33);
    private final int[] a = {1,2,3,4,5,6};
    public String toString(){
        return id + ":"+"i4:"+i4+ " + INT_5="+INT_5;
    }
    void f() {
        FinalData fd1 = new FinalData("fd1");
        fd1.v2.i++;
        fd1.v1 = new Value(9);
        for (int i = 0 ; i < fd1.a.length;i++)
            fd1.a[i]++;
        System.out.println(fd1);
        System.out.println("create new findal");
        FinalData fd2 = new FinalData("fd2");
        System.out.println(fd1);
        System.out.println(fd2);
    }
}

class	Poppet{ //142 初始化空白数据
    private int i;
    Poppet(int  ii){i = ii;}
}
class	BlankFinal	{
    private final	int	i	=	0;	//	Initialized	final
    private final	int	j;	//	Blank	final
    private final	Poppet	p;	//	Blank	final	handle
    public BlankFinal()	{
        j	=	1;	//	Initialize	blank	final
        p	=	new	Poppet(i);
    }
    public BlankFinal(int	x)	{
        j	=	x;	//	Initialize	blank	final
        p	=	new	Poppet(x);
    }
    void f()	{
        new	BlankFinal();
        new BlankFinal(47);
    }
}

class Gizmo{ //142
    public void spin(){}
}
class FinalArguments {
    void with(final Gizmo g){}
    void without(Gizmo g){
        g = new Gizmo();
        g.spin();
    }
    int g (final int i){return i + 1;}
    void f(){
        FinalArguments bf = new FinalArguments();
        bf.with(null);
        bf.without(null);
    }
}

class	SmallBrain	{}// 145 final类不可以继承，也不可以别人修改，里面所有的方法都是final类型的*/
final	class	Dinosaur{
    int	i	=	7;
    int	j	=	1;
    SmallBrain	x	=	new	SmallBrain();
    void	f()	{}
}
class	Jurassic{
    void f(){
        Dinosaur	n	=	new	Dinosaur();
        n.f();
        n.i	=	40;
        System.out.println(n.j++);
    }
}

class	Insect	{// 146 初始化及集成
    int	i	=	9;
    int	j;
    Insect()	{
        prt("i	=	"	+	i	+	",	j	=	"	+	j);
        j	=	39;
    }
    static	int	x1	=
            prt("static	Insect.x1	initialized");
    static	int	prt(String	s) {
        System.out.println(s);
        return	47;
    }
}
class	Beetle	extends	Insect	{
    int	k	=	prt("Beetle.k	initialized");
    Beetle() {
        prt("k	=	"	+	k);
        prt("j	=	"	+	j);
    }
    static	int	x2	=
            prt("static	Beetle.x2	initialized");
    static	int	prt(String	s) {
        System.out.println(s);
        return	63;
    }
    void f() {
        prt("Beetle	constructor");
        Beetle	b	=	new	Beetle();
    }
}

//169 pause no 8zhang








public class book {
    public static void main(String[] args) {

        Beetle be = new Beetle();
        be.f();
//        Jurassic jc = new Jurassic();
//        jc.f();

//        FinalArguments fa = new FinalArguments();
//        fa.f();
//        BlankFinal bk = new BlankFinal();
//        bk.f();
//        FinalData fd = new FinalData("U.S FBI");
//        fd.f();
//        Car c = new Car();
//        c.f();
//        PlaceSetting.f();
//        SpaceShipDelegation sd = new SpaceShipDelegation("U.S SEAL");
//        sd.f();
//        SpaceShip ss = new SpaceShip("U.S NAVY");
//        ss.f();
//        Chess cs = new Chess(11);
//        cs.f();
//        Cartoon ct = new Cartoon();
//        ct.f();
//        Detergent dt = new Detergent();
//        dt.f(args);
//        Bath b = new Bath();
//        b.f();
//        SprinklerSystem ss = new SprinklerSystem();
//        ss.f();
//        Burrito b = new Burrito(Spiciness.HOT);
//        b.f();
//        EnumOrder eo = new EnumOrder();
//        eo.f();
//        SimpleEnumCase sc = new SimpleEnumCase();
//        sc.f();
//        OverloadingVarargs2 ov2 = new OverloadingVarargs2();
//        ov2.f();

//        AutoBoxing ab =  new AutoBoxing();
//        ab.f();
//        VarargType vt = new VarargType();
//        vt.f();
//        ShowPro sh  = new ShowPro();
//        sh.r();
//        OverFlow of = new OverFlow();
//        of.r();
//        ListChar lc = new ListChar();
//        lc.r();
//        CommaOperator co = new CommaOperator();
//        co.r();
//        ForeachString fs = new ForeachString();
//        fs.r();
//        IfElse ie = new IfElse();
//        System.out.println(ie.f(2,3));
//        BreakACon ba = new BreakACon();
//        ba.f();
//        VowelAndCon va = new VowelAndCon();
//        va.f();
//        SimpleCon sc = new SimpleCon();
//        sc.f();
//        Simplecon sc = new Simplecon();
//        sc.f();
//        OverLoading ol = new OverLoading();
//        ol.f();
//        Leaf lf = new Leaf();
//        lf.f();
//        PassingThis pt = new PassingThis();
//        pt.f();
//        Flower f = new Flower();
//        f.f();
//        StaticInit si = new StaticInit();
//        si.f();
//        ExplicitStatic es = new ExplicitStatic();
//        es.f();
//        Mugs ms = new Mugs();
//        ms.f();
//        ArayOfPri ap = new ArayOfPri();
//        ap.f();
//        OptionalTrai op = new OptionalTrai();
//        op.f();
    }
}
