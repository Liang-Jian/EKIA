package com.example.robot.tls;




enum Note{ //170
    MIDDLE_C,C_SHARP,B_FLAT;
}

//abstract class Instrument{
//    private int i;
//    public abstract void play(Note n);
//    public String what() { return "Instrument";}
//    public abstract void adjust(); // 没有{}
//}
//class Wind extends Instrument{
//    @Override
//    public void play(Note n) {
//        System.out.println("wind.play" + n);
//    }
//    @Override
//    public void adjust() {
//    }
//
//    public String what() { return "WINd";}
//}
//class Percussion extends Instrument{
//
//    @Override
//    public void play(Note n) {
//        System.out.println("Percussion" + n);
//    }
//
//    @Override
//    public void adjust() {
//
//    }
//    public String what() { return  "Percussion" ;}
//}
//
//class Stringed extends Instrument{
//
//
//    @Override
//    public void play(Note n) {
//        System.out.println("Strigned" + n);
//    }
//
//    public String what() { return "Stringed";}
//    @Override
//    public void adjust() {
//
//    }
//}
//class Brass extends Wind{
//    public void play(Note n){
//        System.out.println("brass" + n);
//    }
//    public void adjust(){
//        System.out.println("brass.adjust");
//    }
//}
//class Woodwind extends Wind{
//    public void play(Note n){
//        System.out.println("Woodwind.play" + n);
//    }
//    public String what(){ return "wooodwind";}
//}
//class Music4{
//    static void tune(Instrument i){
//        i.play(Note.MIDDLE_C);
//    }
//    static void tuneAll(Instrument[] e ){
//        for (Instrument i:e){
//            tune(i);
//        }
//    }
//    void f(){
//        Instrument[] orchestra = {new Wind(), new Percussion(),new Stringed(),new Brass(),new Woodwind()};
//        tuneAll(orchestra);
//    }
//}
//
//public class book2{
//    public static void main(String[] args) {
//        Music4 m = new Music4();
//        m.f();
//    }
//}
