package seleniumutils;


import java.util.Random;

class extenfx1<T> implements fxin<T> {
    @Override
    public T next(){
        return null;
    }
}


public class extenfx implements fxin<String> {
    private String[] frutis =new String[]{"apple","orange","pea"};
    @Override
    public String next() {
        Random rand = new Random();
        System.out.println(frutis[rand.nextInt(3)]);
        return frutis[rand.nextInt(3)];

    }

    public static void main(String[] args) {
        extenfx ex = new extenfx();
        ex.next();
    }
}
