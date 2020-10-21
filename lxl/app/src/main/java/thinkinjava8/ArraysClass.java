package thinkinjava8;

import java.util.*;

/**
 *  21  chapter
 *  Arrays 数组结构
 *
 */


/*

class BerylliumSphere {
    private static long counter;
    private final long id = counter++;
    @Override
    public String toString() {
        return "Sphere " + id;
    }
}
class CollectionComparison {
    static void f() {
        BerylliumSphere[] spheres =
                new BerylliumSphere[10];
        for(int i = 0; i < 5; i++)
            spheres[i] = new BerylliumSphere();
        show(spheres);
        System.out.println(spheres[4]);

        List<BerylliumSphere> sphereList = Suppliers.create(
                ArrayList::new, BerylliumSphere::new, 5);
        System.out.println(sphereList);
        System.out.println(sphereList.get(4));

        int[] integers = { 0, 1, 2, 3, 4, 5 };
        show(integers);
        System.out.println(integers[4]);

        List<Integer> intList = new ArrayList<>(
                Arrays.asList(0, 1, 2, 3, 4, 5));
        intList.add(97);
        System.out.println(intList);
        System.out.println(intList.get(4));
    }
}

*/




//
interface ArrayShow {
    static void show(Object[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(boolean[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(byte[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(char[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(short[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(int[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(long[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(float[] a) {
            System.out.println(Arrays.toString(a));
            }
    static void show(double[] a) {
            System.out.println(Arrays.toString(a));
            }
    // Start with a description:
    static void show(String info, Object[] a) {
            System.out.print(info + ": ");
        show(a);
        }
    static void show(String info, boolean[] a) {
        System.out.print(info + ": ");
        show(a);
        }
    static void show(String info, byte[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, char[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, short[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, int[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, long[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, float[] a) {
            System.out.print(info + ": ");
            show(a);
            }
    static void show(String info, double[] a) {
        System.out.print(info + ": ");
        show(a);
        }
}




// duowei shuzu
class MultidimensionalPrimitiveArray {
    static void f() {
        int[][] a = {
                { 1, 2, 3, },
                { 4, 5, 6, },
        };
        System.out.println(Arrays.deepToString(a));
    }
}




class ThreeDWithNew {
    static void f() {
        // 3-D array with fixed length:
        int[][][] a = new int[2][2][4];
        System.out.println(Arrays.deepToString(a));
    }
}


public class ArraysClass {
    public static void main(String[] args) {
//        MultidimensionalPrimitiveArray.f();
        ThreeDWithNew.f();
    }
}
