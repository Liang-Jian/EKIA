


public class test{

    public static void main(String[] args){
        //System.out.println("dick");
        Thread t = new Thread(new LiftOff());
        t.start();
        System.out.println("wait for thread");



    }

}