package gittech;


class bignumnber{
    private int number11;
    private int number22;
    public int getnumber() { return  number11 ;}
    public void setnumber(int number11) {this.number11 =number11 ;}
    public int getnumber2() {return number22;}
    public void setnumber22(int number22) {this.number22 = number22;}
    public bignumnber(int number11,int number22){
        this.number11 = number11;
        this.number22 = number22;
    }
    public int add() { return number11 + number22;}
    public int multiply(){return number11 + number22;}
    public void doublevalue(){
        this.number11 += 2;
        this.number22 += 2;
    }
}

public class BiNumber {
    private int number1;
    private int number2;

    public int getNumber1() {
        return number1;
    }

    public void setNumber1(int number1) {
        this.number1 = number1;
    }

    public int getNumber2() {
        return number2;
    }

    public void setNumber2(int number2) {
        this.number2 = number2;
    }

    public BiNumber(int number1, int number2) {
        this.number1 = number1;
        this.number2 = number2;
    }

    public int add() {
        return number1 + number2;
    }

    public int multiply() {
        return number1 * number2;
    }

    public void doubleValue() {
        this.number1 *= 2;
        this.number2 *= 2;
    }
}