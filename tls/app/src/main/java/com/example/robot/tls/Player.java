package com.example.robot.tls;

public class Player {

    private int[] pokers;
    private int index;
    public Player(){
        this.pokers = new int[12] ;
        this.index = 0;
    }

    public boolean wantPokers(int num){
        if (this.index >= 12){
            return  false;
        }
        this.pokers[index] = num;
        index++;

        return true;
    }

    /**
     * 获取当前的点数之和
     * @return
     */
    public int getSum(int a){
        int sum = 0 ;
        for (int i = 0; i < pokers.length; i++) {
            if (pokers[i] == 0){
                break;
            }
            int count =(pokers[i] -1 ) % 13 +1;
//            int color =(pokers[i] -1 ) % 13;
            sum += count;

//            switch (color){
//                case 0:
//                    texts[0] += "黑桃" + count + ",";
//                    break;
//                case 1:
//                    texts[0] += "红桃" + count + ",";
//                    break;
//                case 2:
//                    texts[0] += "梅花" + count + ",";
//                    break;
//                case 3:
//                    texts[0] += "方块" + count + ",";
//                    break;
//            }
        }
        return sum;
    }


    /**
     * 获取当前的点数之和
     * @return
     */
    public int getSum(){
        int sum = 0 ;
        for (int i = 0; i < pokers.length; i++) {
            if (pokers[i] == 0){
                break;
            }
            int count = Pokers.getCount(pokers[i]);
            sum += count;


        }
        return sum;
    }

    public String getStatString(){
        String txt = "";
        for (int i = 0; i < pokers.length; i++) {
            if (pokers[i] == 0){
                break;
            }
            txt += Pokers.getColorString(pokers[i]) + Pokers.getCount(pokers[i]) + ".";
        }return  txt;
    }
}
