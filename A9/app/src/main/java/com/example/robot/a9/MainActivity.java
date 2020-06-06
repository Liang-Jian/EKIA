package com.example.robot.a9;

import android.content.ContentResolver;
import android.database.Cursor;
import android.database.sqlite.SQLiteException;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.view.WindowManager;
import android.widget.Toast;

import java.sql.Date;
import java.text.SimpleDateFormat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.getWindow().addFlags(WindowManager.LayoutParams.FLAG_SECURE);  // 禁止截屏

        try {Thread.sleep(6000);} catch (Exception e) {}
        Toast.makeText(this, "Fuck This World", Toast.LENGTH_SHORT).show();
        try {Thread.sleep(3000);} catch (Exception e) {}
//        Toast.makeText(this, readSMS(), Toast.LENGTH_SHORT).show();


    }

    public String readSMS() {
        final String SMS_URI_ALL   = "content://sms/";
        final String SMS_URI_INBOX = "content://sms/inbox";
        final String SMS_URI_SEND  = "content://sms/sent";
        final String SMS_URI_DRAFT = "content://sms/draft";

        StringBuilder smsBuilder = new StringBuilder();

        try{
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

                do{
                    name = cur.getString(nameColumn);
                    phoneNumber = cur.getString(phoneNumberColumn);
                    smsbody = cur.getString(smsbodyColumn);

                    SimpleDateFormat dateFormat = new SimpleDateFormat(
                            "yyyy-MM-dd hh:mm:ss");
                    Date d = new Date(Long.parseLong(cur.getString(dateColumn)));
                    date = dateFormat.format(d);

                    int typeId = cur.getInt(typeColumn);
                    if(typeId == 1){
                        type = "接收";
                    } else if(typeId == 2){
                        type = "发送";
                    } else {
                        type = "";
                    }

                    smsBuilder.append("[");
                    smsBuilder.append(name+",");
                    smsBuilder.append(phoneNumber+",");
                    smsBuilder.append(smsbody+",");
                    smsBuilder.append(date+",");
                    smsBuilder.append(type);
                    smsBuilder.append("] ");

                    if(smsbody == null) smsbody = "";
                }while(cur.moveToNext());
            } else {
                smsBuilder.append("no result!");
            }

            smsBuilder.append("getSmsInPhone has executed!");
        } catch(SQLiteException ex) {
            Log.d("SQLiteException in getSmsInPhone", ex.getMessage());
        }
        System.out.println(smsBuilder.toString());
        return smsBuilder.toString();
    }



}
