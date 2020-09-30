package thinkinjava8;

import java.util.ArrayList;

/**
 * 7 chapter
 * Access control
 * 封装 /  隐藏实现
 * package
 */





class FullQualification{
    static void f(){}
    java.util.ArrayList list = new java.util.ArrayList<>();
}
class SingleImport{
    static void f(){
        ArrayList list = new ArrayList();
    }
}



class OrganizedByAccess {
    public void pub1() {/* ... */}
    public void pub2() {/* ... */}
    public void pub3() {/* ... */}
    private void priv1() {/* ... */}
    private void priv2() {/* ... */}
    private void priv3() {/* ... */}
    private int i;
}



class Soup1{
    private Soup1(){}
    public static Soup1 makeSoup(){
        return new Soup1();
    }
}
class Soup2{
    private Soup2(){}
    private static Soup2 ps1 = new Soup2();
    public  static Soup2 access(){
        return ps1;
    }
    public void f() {}
}
class Lunch{
    void testPrivate(){}
    void testStatic(){
        Soup1 soup = Soup1.makeSoup();
    }
    void testSingleton(){
        Soup2.access().f();
    }
}









public class implementationhiding {
    public static void main(String[] args) {
        SingleImport.f();

    }
}
