package thinkinjava8;


import java.util.Arrays;

/**
 *  enum 类型
 *  
 *
 *
 */


enum Shrubbery { GROUND, CRAWLING, HANGING }
class EnumClass {
    static void f() {
        for (Shrubbery s : Shrubbery.values()) {
            System.out.println(
                    s + " ordinal: " + s.ordinal());
            System.out.print(
                    s.compareTo(Shrubbery.CRAWLING) + " ");
            System.out.print(
                    s.equals(Shrubbery.CRAWLING) + " ");
            System.out.println(s == Shrubbery.CRAWLING);
            System.out.println(s.getDeclaringClass());
            System.out.println(s.name());
            System.out.println("********************");
        }
// Produce an enum value from a String name:
        for (String s :
                "HANGING CRAWLING GROUND".split(" ")) {
            Shrubbery shrub =
                    Enum.valueOf(Shrubbery.class, s);
            System.out.println(shrub);
        }
    }
}





public class enumclass {
    public static void main(String[] args) {
        EnumClass.f();
    }
}
