package gittech;


public class Book {

    private int noOfCopies;

    public Book(int noOfCopies) {
        this.noOfCopies = noOfCopies;
    }

    public void setNoOfCopies(int noOfCopies) {
        if (noOfCopies > 0)
            this.noOfCopies = noOfCopies;
    }

    public void increaseNoOfCopies(int howMuch) {
        setNoOfCopies(this.noOfCopies + howMuch);
    }

    public void decreaseNoOfCopies(int howMuch) {
        setNoOfCopies(this.noOfCopies - howMuch);
    }

}

class bookcopy{
    private int start;

    public bookcopy(int start) {
        this.start = start;
    }

    public void setstart(int start){
        if (start > 0)
            this.start = start;
    }
    public void increasestart(int howmuch) {setstart(this.start + howmuch);;}
    public void decresedstart(int howmuch) {setstart(this.start - howmuch);;}

}