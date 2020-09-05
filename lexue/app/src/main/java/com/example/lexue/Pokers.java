package com.example.lexue;

public class Pokers {
    private int[] pokers;
    private int index;

    public Pokers(){
        index = 0;
        this.pokers = new int[52];
        for (int i = 1; i <= 52; i++) {
            pokers[i-1]  = i;
        }
        pokers = shuffle(pokers);
    }


    /**
     * 洗牌算法
     * @param nums
     * @return
     */
    int[] shuffle(int[] nums){
        java.util.Random rnd = new java.util.Random();
        for (int i = nums.length-1; i >0; i--) {
            int j =rnd.nextInt(i+1);
            int temp = nums[i];
            nums[i] = nums[j];
            nums[j] = temp;

        }
        return nums;
    }
    public  int getNextPoker(){
        int poker =pokers[index];
        index++;
        return poker;
    }

    /**
     * 获得真正的dianshu
     * @param num
     * @return
     */
    public static int getCount(int num){
        return (num - 1) % 13 +1;
    }

    /**
     *从牌的序号序号中得到花色
     * @param num
     * @return
     */
    public static int getColor(int num){
        return (num - 1) % 13 ;
    }

    /**
     * 从拍的序号中的出花色值的文字表达.
     *
     * @param num
     * @return
     */
    public static String getColorString(int num){
        String txt ="";
        switch (getColor(num)){
            case 0:
                txt = "黑桃";
                break;
            case 1:
                txt = "红桃";
                break;
            case 2:
                txt = "梅花";
                break;
            case 3:
                txt = "方片";
                break;

        }return  txt;
    }
}
