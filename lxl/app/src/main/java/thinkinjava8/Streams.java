package thinkinjava8;

import java.util.stream.*;
import java.util.*;
import java.util.function.*;
import java.io.*;
import java.nio.file.*;
import static java.util.stream.IntStream.*;
import java.util.regex.Pattern;
import static java.util.stream.LongStream.*;
/**
 *
 *  14 chapter
 *  流式编程
 */




//我们给 **Random** 对象一个种子（以便程序再次运行时产生相同的输出）。`ints()` 方法产生一个流并且 `ints()` 方法有多种方式的重载 — 两个参数限定了产生的数值的边界。这将生成一个随机整数流。我们用中间流操作（intermediate stream operation） `distinct()` 使流中的整数不重复，然后使用 `limit()` 方法获取前 7 个元素。接下来使用 `sorted()` 方法排序。最终使用 `forEach()` 方法遍历输出，它根据传递给它的函数对流中的每个对象执行操作。在这里，我们传递了一个可以在控制台显示每个元素的方法引用：`System.out::println` 。
class Randoms {
    static void f() {
        new Random(47)
                .ints(5, 20)
                .distinct()
                .limit(7)
                .sorted()
                .forEach(System.out::println);
    }
}





class ImperativeRandoms{
    static void f() {
        Random rand = new Random(47);
        SortedSet<Integer> rints = new TreeSet<>();
        while(rints.size() < 7) {
            int r = rand.nextInt(20);
            if(r < 5) continue;
            rints.add(r);
        }
        System.out.println(rints);
    }
}





/*class StreamOf {
    static void f() {
        Stream.of(new Bubble(1), new Bubble(2), new Bubble(3))
                .forEach(System.out::println);
        Stream.of("It's ", "a ", "wonderful ", "day ", "for ", "pie!")
                .forEach(System.out::print);
        System.out.println();
        Stream.of(3.14159, 2.718, 1.618).forEach(System.out::println);

    }
}*/




//随机数流
class RandomGenerators {
    public static <T> void show(Stream<T> stream) {
        stream
                .limit(4)
                .forEach(System.out::println);
        System.out.println("++++++++");
    }

    static void f() {
        Random rand = new Random(47);
        show(rand.ints().boxed());
        show(rand.longs().boxed());
        show(rand.doubles().boxed());
        // 控制上限和下限：
        show(rand.ints(10, 20).boxed());
        show(rand.longs(50, 100).boxed());
        show(rand.doubles(20, 30).boxed());
        // 控制流大小：
        show(rand.ints(2).boxed());
        show(rand.longs(2).boxed());
        show(rand.doubles(2).boxed());
        // 控制流的大小和界限
        show(rand.ints(3, 3, 9).boxed());
        show(rand.longs(3, 12, 22).boxed());
        show(rand.doubles(3, 11.5, 12.3).boxed());
    }
}




/*
class RandomWords implements Supplier<String> {
    List<String> words = new ArrayList<>();
    Random rand = new Random(47);
    RandomWords(String fname) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(fname));
        // 略过第一行
        for (String line : lines.subList(1, lines.size())) {
            for (String word : line.split("[ .?,]+"))
                words.add(word.toLowerCase());
        }
    }
    public String get() {
        return words.get(rand.nextInt(words.size()));
    }
    @Override
    public String toString() {
        return words.stream()
                .collect(Collectors.joining(" "));
    }
    public static void f() throws Exception {
        try {
            System.out.println(
                    Stream.generate(new RandomWords("Cheese.dat"))
                            .limit(10)
                            .collect(Collectors.joining(" ")));
        }catch (Exception e){e.printStackTrace();}

    }
}*/



//`IntStream` 类提供了  `range()` 方法用于生成整型序列的流。编写循环时，这个方法会更加便利：
class Ranges {
    static void f() {
        // 传统方法:
        int result = 0;
        for (int i = 10; i < 20; i++)
            result += i;
        System.out.println(result);
        // for-in 循环:
        result = 0;
        for (int i : range(10, 20).toArray())
            result += i;
        System.out.println(result);
        // 使用流:
        System.out.println(range(10, 20).sum());
    }
}



class Repeat {
    public static void repeat(int n, Runnable action) {
        range(0, n).forEach(i -> action.run());
    }
}
class Looping {
    static void hi() {
        System.out.println("Hi!");
    }
    static void f() {
        Repeat.repeat(3, () -> System.out.println("Looping!"));
        Repeat.repeat(2, Looping::hi);
    }
}



//使用 `Random.nextInt()` 方法来挑选字母表中的大写字母。`Random.nextInt()` 的参数代表可以接受的最大的随机数范围，所以使用数组边界是经过深思熟虑的。
class Generator implements Supplier<String> {
    Random rand = new Random(47);
    char[] letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();

    public String get() {
        return "" + letters[rand.nextInt(letters.length)];
    }

    static void f() {
        String word = Stream.generate(new Generator())
                .limit(30)
                .collect(Collectors.joining());
        System.out.println(word);
    }
}




//
class Duplicator{
    static void f() {
        Stream.generate(() -> "duplicate")
                .limit(3)
                .forEach(System.out::println);
    }
}




//创建单独工厂类（Separate Factory class）的另一种方式。在很多方面它更加整洁，但是这是一个对于代码组织和品味的问题——你总是可以创建一个完全不同的工厂类。
class Bubble {
    public final int i;

    public Bubble(int n) {
        i = n;
    }

    @Override
    public String toString() {
        return "Bubble(" + i + ")";
    }

    private static int count = 0;
    public static Bubble bubbler() {
        return new Bubble(count++);
    }
}
class Bubbles {
    static void f() {
        Stream.generate(Bubble::bubbler)
                .limit(5)
                .forEach(System.out::println);
    }
}




//斐波那契数列将数列中最后两个元素进行求和以产生下一个元素。`iterate()` 只能记忆结果，因此我们需要利用一个变量 `x` 追踪另外一个元素。
class Fibonacci{
    int x = 1;
    Stream<Integer> numbers() {
        return Stream.iterate(0, i -> {
            int result = x + i;
            x = i;
            return result;
        });
    }
    static void f() {
        new Fibonacci().numbers()
                .skip(20) // 过滤前 20 个
                .limit(10) // 然后取 10 个
                .forEach(System.out::println);
    }
}





class FileToWordsBuilder{
    Stream.Builder<String> builder = Stream.builder();
    public FileToWordsBuilder(String filePath) throws Exception {
        Files.lines(Paths.get(filePath))
                .skip(1) // 略过开头的注释行
                .forEach(line -> {
                    for (String w : line.split("[ .?,]+"))
                        builder.add(w);
                });
    }

    Stream<String> stream() {
        return builder.build();
    }

    static void f() throws Exception {
        new FileToWordsBuilder("Cheese.dat")
                .stream()
                .limit(7)
                .map(w -> w + " ")
                .forEach(System.out::print);
    }
}




class Machine2 {
    static void f() {
        Arrays.stream(new Operations[] {
                () -> Operations.show("Bing"),
                () -> Operations.show("Crack"),
                () -> Operations.show("Twist"),
                () -> Operations.show("Pop")
        }).forEach(Operations::execute);
    }
}





class ArrayStreams {
    static void f() {
        Arrays.stream(new double[] { 3.14159, 2.718, 1.618 })
                .forEach(n -> System.out.format("%f ", n));
        System.out.println();

        Arrays.stream(new int[] { 1, 3, 5 })
                .forEach(n -> System.out.format("%d ", n));
        System.out.println();

        Arrays.stream(new long[] { 11, 22, 44, 66 })
                .forEach(n -> System.out.format("%d ", n));
        System.out.println();

        // 选择一个子域:
        Arrays.stream(new int[] { 1, 3, 5, 7, 15, 28, 37 }, 3, 6)
                .forEach(n -> System.out.format("%d ", n));
    }
}




class FileToWordsRegexp {
    private String all;
    public FileToWordsRegexp(String filePath) throws Exception {
        all = Files.lines(Paths.get(filePath))
                .skip(1) // First (comment) line
                .collect(Collectors.joining(" "));
    }
    public Stream<String> stream() {
        return Pattern
                .compile("[ .,?]+").splitAsStream(all);
    }
    static void
    f(String[] args) throws Exception {
        FileToWordsRegexp fw = new FileToWordsRegexp("Cheese.dat");
        fw.stream()
                .limit(7)
                .map(w -> w + " ")
                .forEach(System.out::print);
        fw.stream()
                .skip(7)
                .limit(2)
                .map(w -> w + " ")
                .forEach(System.out::print);
    }
}




/*
class Peeking {
public static void main(String[] args) throws Exception {
        FileToWords.stream("Cheese.dat")
        .skip(21)
        .limit(4)
        .map(w -> w + " ")
        .peek(System.out::print)
        .map(String::toUpperCase)
        .peek(System.out::print)
        .map(String::toLowerCase)
        .forEach(System.out::print);
        }
}
*/



/*
class SortedComparator {
    public static void main(String[] args) throws Exception {
        FileToWords.stream("Cheese.dat")
                .skip(10)
                .limit(10)
                .sorted(Comparator.reverseOrder())
                .map(w -> w + " ")
                .forEach(System.out::print);
    }
}*/



/*

class Prime {
    public static Boolean isPrime(long n) {
        return rangeClosed(2, (long)Math.sqrt(n))
                .noneMatch(i -> n % i == 0);
    }
    public LongStream numbers() {
        return iterate(2, i -> i + 1)
                .filter(Prime::isPrime);
    }
    public static void main(String[] args) {
        new Prime().numbers()
                .limit(10)
                .forEach(n -> System.out.format("%d ", n));
        System.out.println();
        new Prime().numbers()
                .skip(90)
                .limit(10)
                .forEach(n -> System.out.format("%d ", n));
    }
}
 */


class FunctionMap {
    static String[] elements = { "12", "", "23", "45" };
    static Stream<String>
    testStream() {
        return Arrays.stream(elements);
    }
    static void test(String descr, Function<String, String> func) {
        System.out.println(" ---( " + descr + " )---");
        testStream()
        .map(func)
        .forEach(System.out::println);
    }
    static void f() {
        test("add brackets", s -> "[" + s + "]");
        test("Increment", s -> {
            try {
                return Integer.parseInt(s) + 1 + "";
            }
            catch(NumberFormatException e) {
                return s;
            }
        }
        );
        test("Replace", s -> s.replace("2", "9"));
        test("Take last digit", s -> s.length() > 0 ?
        s.charAt(s.length() - 1) + "" : s);
    }
}




//`map()` 将一个字符串映射为另一个字符串，但是我们完全可以产生和接收类型完全不同的类型，从而改变流的数据类型。
class Numbered {
    final int n;
    Numbered(int n) {
        this.n = n;
    }
    @Override
    public String toString() {
        return "Numbered(" + n + ")";
    }
}
class FunctionMap2 {
    static void f() {
        Stream.of(1, 5, 7, 9, 11, 13)
                .map(Numbered::new)
                .forEach(System.out::println);
    }
}




//
class FunctionMap3 {
     static void f() {
        Stream.of("5", "7", "9")
                .mapToInt(Integer::parseInt)
                .forEach(n -> System.out.format("%d ", n));
        System.out.println();
        Stream.of("17", "19", "23")
                .mapToLong(Long::parseLong)
                .forEach(n -> System.out.format("%d ", n));
        System.out.println();
        Stream.of("17", "1.9", ".23")
                .mapToDouble(Double::parseDouble)
                .forEach(n -> System.out.format("%f ", n));
    }
}





//
class StreamOfStreams{
    static void f() {
        Stream.of(1, 2, 3)
                .map(i -> Stream.of("Gonzo", "Kermit", "Beaker"))
                .map(e-> e.getClass().getName())
                .forEach(System.out::println);
    }
}




//
class FlatMap{
    static void f() {
        Stream.of(1, 2, 3)
                .flatMap(i -> Stream.of("Gonzo", "Fozzie", "Beaker"))
                .forEach(System.out::println);
    }
}


//
class StreamOfRandoms {
    static Random rand = new Random(47);
    static void f() {
        Stream.of(1, 2, 3, 4, 5)
                .flatMapToInt(i -> IntStream.concat(
                        rand.ints(0, 100).limit(i), IntStream.of(-1)))
                .forEach(n -> System.out.format("%d ", n));
    }
}




//
class FileToWords {
    public static Stream<String> stream(String filePath) throws Exception {
        return Files.lines(Paths.get(filePath))
                .skip(1) // First (comment) line
                .flatMap(line ->
                        Pattern.compile("\\W+").splitAsStream(line));
    }
}





//
class FileToWordsTest{
    static void f() throws Exception {
        FileToWords.stream("Cheese.dat")
                .limit(7)
                .forEach(s -> System.out.format("%s ", s));
        System.out.println();
        FileToWords.stream("Cheese.dat")
                .skip(7)
                .limit(2)
                .forEach(s -> System.out.format("%s ", s));
    }
}



//
class OptionalsFromEmptyStreams {
    static void f() {
        System.out.println(Stream.<String>empty()
                .findFirst());
        System.out.println(Stream.<String>empty()
                .findAny());
        System.out.println(Stream.<String>empty()
                .max(String.CASE_INSENSITIVE_ORDER));
        System.out.println(Stream.<String>empty()
                .min(String.CASE_INSENSITIVE_ORDER));
        System.out.println(Stream.<String>empty()
                .reduce((s1, s2) -> s1 + s2));
        System.out.println(IntStream.empty()
                .average());
    }
}



//
class OptionalBasics {
    static void test(Optional<String> optString) {
        if(optString.isPresent())
            System.out.println(optString.get());
        else
            System.out.println("Nothing inside!");
    }
    static void f() {
        test(Stream.of("Epithets").findFirst());
        test(Stream.<String>empty().findFirst());
    }
}





// 便利函数
class Optionals {
    static void basics(Optional<String> optString) {
        if(optString.isPresent())
            System.out.println(optString.get());
        else
            System.out.println("Nothing inside!");
    }
    static void ifPresent(Optional<String> optString) {
        optString.ifPresent(System.out::println);
    }
    static void orElse(Optional<String> optString) {
        System.out.println(optString.orElse("Nada"));
    }
    static void orElseGet(Optional<String> optString) {
        System.out.println(
                optString.orElseGet(() -> "Generated"));
    }
    static void orElseThrow(Optional<String> optString) {
        try {
            System.out.println(optString.orElseThrow(
                    () -> new Exception("Supplied")));
        } catch(Exception e) {
            System.out.println("Caught " + e);
        }
    }
    static void test(String testName, Consumer<Optional<String>> cos) {
        System.out.println(" === " + testName + " === ");
        cos.accept(Stream.of("Epithets").findFirst());
        cos.accept(Stream.<String>empty().findFirst());
    }
    static void f() {
        test("basics", Optionals::basics);
        test("ifPresent", Optionals::ifPresent);
        test("orElse", Optionals::orElse);
        test("orElseGet", Optionals::orElseGet);
        test("orElseThrow", Optionals::orElseThrow);
    }
}




//
class CreatingOptionals {
    static void test(String testName, Optional<String> opt) {
        System.out.println(" === " + testName + " === ");
        System.out.println(opt.orElse("Null"));
    }
    static void f() {
        test("empty", Optional.empty());
        test("of", Optional.of("Howdy"));
        try {
            test("of", Optional.of(null));
        } catch(Exception e) {
            System.out.println(e);
        }
        test("ofNullable", Optional.ofNullable("Hi"));
        test("ofNullable", Optional.ofNullable(null));
    }
}
class Streams {
    public static void main(String[] args) {
//        Randoms.f();
//        ImperativeRandoms.f();
//        StreamOf.f();
//        RandomGenerators.f();
//        RandomWords.f();
//        Ranges.f();
//        Looping.f();
//        Generator.f();
//        Duplicator.f();
//        Bubbles.f();
//        Fibonacci.f();
//        ArrayStreams.f();
//        FileToWordsRegexp.f();
//        FunctionMap.f();
//        FunctionMap2.f();
//        FunctionMap3.f();
//        StreamOfStreams.f();
//        FlatMap.f();
//        StreamOfRandoms.f();
//        FileToWordsTest.f();
//        OptionalsFromEmptyStreams.f();
//        OptionalBasics.f();
//        Optionals.f();
        CreatingOptionals.f();
    }
}
