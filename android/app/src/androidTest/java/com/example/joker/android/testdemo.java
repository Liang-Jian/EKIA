package com.example.joker.android;


import android.app.Instrumentation;
import android.content.Context;
import android.content.Intent;
import android.graphics.Point;
import android.net.wifi.WifiManager;
import android.os.RemoteException;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;
import android.support.test.uiautomator.By;
import android.support.test.uiautomator.UiDevice;
import android.support.test.uiautomator.UiObject;
import android.support.test.uiautomator.UiObject2;
import android.support.test.uiautomator.UiObjectNotFoundException;
import android.support.test.uiautomator.UiSelector;
import android.util.Log;
import org.junit.Test;
import org.junit.runner.RunWith;

import java.io.File;
import java.io.IOException;
import android.net.Uri;
import android.database.Cursor;
import java.text.SimpleDateFormat;
import android.database.sqlite.SQLiteException;
import android.webkit.WebView;

import java.sql.Date;


@RunWith(AndroidJUnit4.class)
public class testdemo extends Instrumentation {
    public UiDevice mDevice;
    public Instrumentation instrumentation;
    private  void Sleep(int timeout){
        try {
            Thread.sleep(timeout);
        }catch (Exception e){}
    }

    private static final int  LAUNCH_TIMEOUT= 7000;
    private static final String SMSPACKAGENAME = "com.google.android.apps.messaging";
    private static final String ACTIVITENAME = "com.google.android.apps.messaging.ui.ConversationListActivity";

    @Test
    public void testClick() {
        instrumentation = InstrumentationRegistry.getInstrumentation();
        UiDevice.getInstance(instrumentation).pressHome();
        Integer k = UiDevice.getInstance(instrumentation).getDisplayHeight();
        Integer k1 = UiDevice.getInstance(instrumentation).getDisplayWidth();
//        Log.d(TAG, "testHome: ");
        Log.i("手机高度", String.valueOf(k));
        Log.i("手机宽度",String.valueOf(k1));
        UiDevice.getInstance(instrumentation).pressMenu();
    }

    @Test
    public void testunlockScreen() throws IOException {//解锁手机屏幕
        UiDevice mDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation()); //声明一个实例对象
        try {
            if (!mDevice.isScreenOn()) {
                mDevice.wakeUp();
            }
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        mDevice.pressMenu();
        Sleep(1000);
        mDevice.swipe(525, 1414, 525, 580, 10); //滑动解锁时距离过长，影响解锁
//        mDevice.takeScreenshot(new File("/sdcard/Download/a.JPG")); //截图函数,传递过去一个对像
        Sleep(1000);
        mDevice.executeShellCommand("screencap -p  /mnt/sdcard/123.png"); //使用adb命令来做的截图,最好强制停止1s,因为可能速度较快，截图发白

        //driver.findElementByAndroidUIAutomator( "new UiSelector().text(\"Test222邮件123xfm8c1o5\").fromParent(new UiSelector().className(\"android.widget.TextView\").index(4))").getText();
//        mDevice.getLauncherPackageName();
        Log.i("包名是: ",mDevice.getCurrentPackageName());
        Log.i("动名是: ",mDevice.getCurrentActivityName());
    }

/*    @Test
    public void TestCase1(){
        File file =new file("/storage/self/primary/DCIM/100ANDRO/a.JPG");
        Log.i(TAG, "TestCase1: file path = " + file.getPath());
        mDevice.takeScreenshot(new File("/storage/self/primary/DCIM/100ANDRO/a.JPG"));
        mDevice.waitForIdle();
    }*/

    @Test
    public void testSetting() throws UiObjectNotFoundException {
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        UiObject setterobject = new UiObject(new UiSelector().textContains("10086"));
        Sleep(1000);
        setterobject.clickAndWaitForNewWindow(); //只针对当前显示
        UiObject duanxininput = new UiObject(new UiSelector().className("android.widget.EditText"));
        duanxininput.setText("fuck");
        UiObject senD = new UiObject(new UiSelector().className("android.widget.ImageButton"));
        senD.click();
        Log.i("包名",uiDevice.getCurrentPackageName());
    }
    private void startAPP(String sPackageName){ //根据报名启动apk ,
        Context mContext = InstrumentationRegistry.getContext();
        Intent myIntent = mContext.getPackageManager().getLaunchIntentForPackage(sPackageName);  //通过Intent启动app
        mContext.startActivity(myIntent);
    }
    @Test
    public void teststartAPP() throws UiObjectNotFoundException{
        UiDevice uiDevice  = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        UiObject setterobject = new UiObject(new UiSelector().textContains("10086"));
        try {
            if(!uiDevice.isScreenOn()){
                uiDevice.wakeUp();
            }
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        startAPP(SMSPACKAGENAME);
        uiDevice.waitForWindowUpdate(SMSPACKAGENAME,3 * 1000);
        Sleep(1000);
        setterobject.clickAndWaitForNewWindow(); //只针对当前显示
        UiObject duanxininput = new UiObject(new UiSelector().className("android.widget.EditText"));
        duanxininput.setText("fuck");
        UiObject senD = new UiObject(new UiSelector().className("android.widget.ImageView"));
        senD.click();
        Log.i("包名",uiDevice.getCurrentPackageName());
    }



    @Test
    public void setWifi(){ //  切换wifi三次
        WifiManager mwm = (WifiManager) InstrumentationRegistry.getContext().getSystemService(Context.WIFI_SERVICE);
        int Start = 0;
        while(Start < 3){
            Start++;
//            System.out.println(mwm);
            Boolean state = mwm.isWifiEnabled();
            state = !state;
            mwm.setWifiEnabled(state);
        }
    }
    @Test
    public void testsms() throws UiObjectNotFoundException { //使用uiobject 发送短信
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
//        UiObject setterobject = new UiObject(new UiSelector().textContains("10690935167259227441"));
        UiObject setterobject = new UiObject(new UiSelector().textContains("10086"));
        uiDevice.waitForWindowUpdate(SMSPACKAGENAME,3 * 1000);
        Sleep(1000);
        setterobject.clickAndWaitForNewWindow(); //只针对当前显示
        UiObject duanxininput = new UiObject(new UiSelector().className("android.widget.EditText"));
        duanxininput.setText("fuck");
        UiObject sendsms = new UiObject(new UiSelector().resourceId("com.google.android.apps.messaging:id/send_message_button_icon"));
        sendsms.click();
        Log.i("包名",uiDevice.getCurrentPackageName());

    }
    @Test
    public void smsnew(){ //UiObject2 来定位元素
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        UiObject2 smsnm  = uiDevice.findObject(By.res("com.google.android.apps.messaging:id/conversation_name"));
        uiDevice.waitForWindowUpdate(SMSPACKAGENAME,3*1000);
        UiObject2 editmm = uiDevice.findObject(By.res("com.google.android.apps.messaging:id/compose_message_text"));
        UiObject2 smssend = uiDevice.findObject(By.res("com.google.android.apps.messaging:id/send_message_button_icon"));

        smsnm.click();
        Sleep(3000);
//        System.out.println(editmm.getText());
        editmm.setText("fuck");
        smssend.click();


    }

    @Test
    public void clickwz(){
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
        while (true){
            uiDevice.click(880,944);
            Sleep(13000);
            uiDevice.click(965,805);
        }

//        UiObject2 smsnm  = uiDevice.findObject(By.res("com.google.android.apps.messaging:id/conversation_name"));
    }

    @Test
    public void mingwen() throws  Exception{
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());

        int startx = 300;
        int starty = 863;


        int start = 0;
        while (start < 100){

            uiDevice.click(1725,937);
            uiDevice.click(1725,937);
            Sleep(1500);
            Thread.sleep(1000);
            uiDevice.drag(startx,starty,startx,starty-200,150);
            start++;
//                        uiDevice.swipe(startx,starty,startx,starty-200,150); //up
//            uiDevice.swipe(startx,starty,startx,starty+200,100); //down

//            Sleep(500);
        }

//        UiObject2 smsnm  = uiDevice.findObject(By.res("com.google.android.apps.messaging:id/conversation_name"));
    }
    @Test
    public void te() throws RemoteException {
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());

        uiDevice.wakeUp();              //唤醒屏幕
//        uiDevice.pressRecentApps();     //切换app 库  口
//        uiDevice.openQuickSettings();   //快速配置,向下滑出设置
        uiDevice.freezeRotation();      //?
//        uiDevice.sleep();               // 熄屏
        uiDevice.isNaturalOrientation();
        uiDevice.openNotification();  //打开消息
        String s = uiDevice.getProductName(); //产品型号F332
        uiDevice.getDisplayHeight();
        uiDevice.getDisplayRotation();
        uiDevice.getDisplaySizeDp();
        uiDevice.getDisplayWidth();
//        int i = uiDevice.getDisplayWidth();
        String si = String.valueOf(uiDevice.getDisplayWidth());
        System.out.println("=====");
        System.out.println(si);
    }

    @Test
    public void cutScreen() throws RemoteException, IOException {
        UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
//        uiDevice.pressHome(); // home键
//        uiDevice.pressSearch(); // 出现搜索框
//        uiDevice.pressRecentApps();  //app抽屉
//        uiDevice.pressDPadCenter();  // no
//        uiDevice.pressDPadDown();    // no
//        uiDevice.pressEnter();       // 如果是抽屉，就会取得刚才的app界面
        Runtime.getRuntime().exec("input keyevent --longpress  5 26");
        Sleep(6000);
        uiDevice.pressKeyCode(26);
        deleting("/sdcard/Download/a.txt");
        String s = uiDevice.executeShellCommand("pwd ; ls");
        System.out.println(s);

    }



    void deleting(String path){
        File file = new File(path);
        file.delete();
    }

//    public void longclickUiObectByResourceId(String id) throws UiObjectNotFoundException {
//
//        int x = getUiObjectByResourceId(id).getBounds().centerX();
//        int y = getUiObjectByResourceId(id).getBounds().centerY();
//        UiDevice.getInstance().swipe(x, y, x, y, 300);//最后一个参数单位是5ms
//    }
//    public void longclickUiObectByText(String text) throws UiObjectNotFoundException {
//        int x = getUiObjectByText(text).getBounds().centerX();
//        int y = getUiObjectByText(text).getBounds().centerY();
//        UiDevice.getInstance().swipe(x, y, x, y, 300);//最后一个参数单位是5ms
//    }

    @Test
    public void unlockscreen(){
        UiDevice mDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation()); //声明一个实例对象
//        try {
//            Runtime.getRuntime().exec("input keyevent  KEYCODE_POWER");
//        }catch (Exception e ) {e.printStackTrace();}
        try{
            mDevice.executeShellCommand("input keyevent  KEYCODE_POWER");  //模拟物理按键 。
        }catch (Exception e) {}
        Sleep(500);
        try {
            if (!mDevice.isScreenOn()) {
                mDevice.wakeUp();
            }
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        mDevice.pressMenu();
        Sleep(1000);
//      mDevice.swipe(525, 1414, 525, 580, 10); //滑动解锁时距离过长，影响解锁

        //解锁流程
        Point p1 = new Point();
        Point p2 = new Point();
        Point p3 = new Point();
        Point p4 = new Point();
        Point p5 = new Point();
        p1.x = 546;p1.y=792;
        p2.x = 546;p2.y=1079;
        p3.x = 546;p3.y=1405;
        p4.x = 839;p4.y=1395;
        p5.x = 839;p5.y=1395;
        Point[] p = {p1,p2,p3,p4,p5,p5};
//        Point[][] p = {{p3,p4},{p1,p2}};
        mDevice.swipe(p,150);
        Sleep(1500);
        UiObject2 ui = mDevice.findObject(By.res("com.sonyericsson.advancedwidget.clock:id/date"));
        Log.i("unlockscreen: ui.getText() {}",ui.getText());
        Log.i("unlockscreen: ui.getApplicationPackage()",ui.getApplicationPackage());
        Log.i("unlockscreen: ui.getClassName",ui.getClassName());
        Log.i("unlockscreen: ui.getResourceName()",ui.getResourceName());

        System.out.println(ui.getText());

    }

    @Test
    public void shuajinbi() throws InterruptedException {//刷金币。
        UiDevice mDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation()); //声明一个实例对象
//        Point p1 = new Point();
//        Point p2 = new Point();
//        Point p3 = new Point();
//        Point p4 = new Point();
//        Point p5 = new Point();
//        p1.x = 277;p1.y=872;
//        p2.x =p1.x+100;p2.y=p1.y-200;
//        Point[] p = {p1,p2};
//        while (true){
//            mDevice.swipe(p,200);
//            Thread.sleep(250);
//            mDevice.click(1725,937);
//
//        }
        Point p1 = new Point();
        Point p2 = new Point();
        p1.x = 277;p1.y=872;
        p2.x =p1.x+100;p2.y=p1.y;
        Point[] p = {p1,p2};
        for (int i=0 ; i < 20000 ; i++){
            mDevice.click(1629,1011); //再次挑战
            Sleep(1000);
            mDevice.click(1419,885);  //闯关
            Sleep(20000);

            int n =0;
            while (n < 110){
                n++;
                mDevice.swipe(p,20);
                Sleep(100);
                mDevice.click(1725,937);

            }
            mDevice.click(941,993);   //点击屏幕继续
        }
    }
    @Test
    public void calc(){ //测试计算器
        UiDevice mDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation()); //声明一个实例对象
        String pn = "com.android.calculator2";
        startAPP(pn);
        mDevice.waitForWindowUpdate(pn,200);
        Sleep(1000);
        //  5 * 9 = 45

        UiObject2 five = mDevice.findObject(By.res("com.android.calculator2:id/digit_5"));
        UiObject2 cheng = mDevice.findObject(By.res("com.android.calculator2:id/op_mul"));
        UiObject2 jiu = mDevice.findObject(By.res("com.android.calculator2:id/digit_9"));
        UiObject2 deng = mDevice.findObject(By.text("="));
        five.click();
        cheng.click();
        jiu.click();
        deng.click();
    }

    @Test
    public void getSmsInPhone() {
        final String SMS_URI_ALL = "content://sms/"; // 所有短信
        final String SMS_URI_INBOX = "content://sms/inbox"; // 收件箱
        final String SMS_URI_SEND = "content://sms/sent"; // 已发送
        final String SMS_URI_DRAFT = "content://sms/draft"; // 草稿
        final String SMS_URI_OUTBOX = "content://sms/outbox"; // 发件箱
        final String SMS_URI_FAILED = "content://sms/failed"; // 发送失败
        final String SMS_URI_QUEUED = "content://sms/queued"; // 待发送列表

        StringBuilder smsBuilder = new StringBuilder();

        try {
            Uri uri = Uri.parse(SMS_URI_ALL);
            String[] projection = new String[] { "_id", "address", "person",
                    "body", "date", "type", };
            Cursor cur = getContext().getContentResolver().query(uri, projection, null,
                    null, "date desc"); // 获取手机内部短信

            // 获取短信中最新的未读短信
            // Cursor cur = getContentResolver().query(uri, projection,
            // "read = ?", new String[]{"0"}, "date desc");
            if (cur.moveToFirst()) {
                int index_Address = cur.getColumnIndex("address");
                int index_Person = cur.getColumnIndex("person");
                int index_Body = cur.getColumnIndex("body");
                int index_Date = cur.getColumnIndex("date");
                int index_Type = cur.getColumnIndex("type");

                do {
                    String strAddress = cur.getString(index_Address);
                    int intPerson = cur.getInt(index_Person);
                    String strbody = cur.getString(index_Body);
                    long longDate = cur.getLong(index_Date);
                    int intType = cur.getInt(index_Type);

                    SimpleDateFormat dateFormat = new SimpleDateFormat(
                            "yyyy-MM-dd hh:mm:ss");
                    Date d = new Date(longDate);
                    String strDate = dateFormat.format(d);

                    String strType = "";
                    if (intType == 1) {
                        strType = "接收";
                    } else if (intType == 2) {
                        strType = "发送";
                    } else if (intType == 3) {
                        strType = "草稿";
                    } else if (intType == 4) {
                        strType = "发件箱";
                    } else if (intType == 5) {
                        strType = "发送失败";
                    } else if (intType == 6) {
                        strType = "待发送列表";
                    } else if (intType == 0) {
                        strType = "所以短信";
                    } else {
                        strType = "null";
                    }

                    smsBuilder.append("[ ");
                    smsBuilder.append(strAddress + ", ");
                    smsBuilder.append(intPerson + ", ");
                    smsBuilder.append(strbody + ", ");
                    smsBuilder.append(strDate + ", ");
                    smsBuilder.append(strType);
                    smsBuilder.append(" ]\n\n");
                } while (cur.moveToNext());

                if (!cur.isClosed()) {
                    cur.close();
                    cur = null;
                }
            } else {
                smsBuilder.append("no result!");
            }

            smsBuilder.append("getSmsInPhone has executed!");

        } catch (SQLiteException ex) {
            Log.d("SQLiteException in getSmsInPhone", ex.getMessage());
        }

        System.out.println(smsBuilder.toString());
//        return smsBuilder.toString();
    }

    @Test
    public void readSMS() {

        final String SMS_URI_ALL = "content://sms/"; // 所有短信
        final String SMS_URI_INBOX = "content://sms/inbox"; // 收件箱
        final String SMS_URI_SEND = "content://sms/sent"; // 已发送
        final String SMS_URI_DRAFT = "content://sms/draft"; // 草稿
        final String SMS_URI_OUTBOX = "content://sms/outbox"; // 发件箱
        final String SMS_URI_FAILED = "content://sms/failed"; // 发送失败
        final String SMS_URI_QUEUED = "content://sms/queued"; // 待发送列表
        startAPP(SMSPACKAGENAME);
//        Cursor cursor = getContext().getContentResolver().query(Uri.parse(SMS_URI_INBOX), null, null, null, null);
        Cursor cursor = getContext().getContentResolver().query(Uri.parse(SMS_URI_INBOX),null,null,null);
        if (cursor.moveToFirst()) { // must check the result to prevent exception
            do {
                String msgData = "";
                for (int idx = 0; idx < cursor.getColumnCount(); idx++) {
                    msgData += " " + cursor.getColumnName(idx) + ":" + cursor.getString(idx);
                }
                // use msgData
            } while (cursor.moveToNext());
        } else {
            // empty box, no SMS}
        }
    }

//    public void openOtherApp(){
//        ComponentName componentName = new ComponentName(SMSPACKAGENAME,ACTIVITENAME);
//        Intent intent = new Intent();
//        intent.setComponent(componentName);
//        startActivitySync(intent);startActivityForResult(intent,1);
//    }



}
