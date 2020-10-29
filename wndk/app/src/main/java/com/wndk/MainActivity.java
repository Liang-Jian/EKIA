package com.wndk;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.view.animation.LinearInterpolator;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import com.google.zxing.activity.CaptureActivity;
import com.google.zxing.util.Constant;


/**
 *  create by : j0ker
 *  北京健康宝伪装程序。为了便利，方便父母使用。我爸妈不会用pk健康宝
 *
 *  台下人走过 不见旧颜色
 *  台上人唱着 心碎离别歌
 *
 */

public class MainActivity extends AppCompatActivity {

    // Used to load the 'native-lib' library on application startup.
    static {
        System.loadLibrary("wndk");
    }

    /**
     * A native method that is implemented by the 'native-lib' native library,
     * which is packaged with this application.
     */
    public native String stringFromJNI();

    public native String helloWorld();

    private TextView timeview;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);//去除标题栏
        setContentView(R.layout.activity_main);

        initView();
        setTouMing();
        addClick();
        // Example of a call to a native method
//        new TimeThread().start(); //启动新的线程
    }


    class TimeThread extends Thread {
        //重写run方法
        @Override
        public void run() {
            super.run();
            // do-while  一 什么什么 就
            do {
                try {
                    //每隔一秒 发送一次消息
                    Thread.sleep(1000);
                    Message msg = new Message();
                    //消息内容 为MSG_ONE
                    msg.what = 1;
                    //发送
                    handler.sendMessage(msg);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            } while (true);
        }
    }

    private void initView() {
//        timeview = findViewById(R.id.tv);

    }

    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {

            super.handleMessage(msg);
            switch (msg.what) {
                case 1:
                    long sysTime = System.currentTimeMillis();
                    CharSequence sysTimeStr = DateFormat.format("hh:mm:ss", sysTime);
                    timeview.setText(sysTimeStr); //更新时间
                    Log.i(" sysTimeStr", sysTimeStr.toString());
                    break;
                default:
                    break;

            }
        }
    };

    public void setTouMing() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            getWindow().addFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
//            getWindow().addFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_NAVIGATION);
        }
    }

    public void addClick() {
        ImageView iv = findViewById(R.id.imageView);
        iv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                jumpcamera();
//                getcode();
            }
        });

    }

    /**
     * 跳轉第二個activity
     */
    public void jumpcamera() {
        // 调用拍照 5s后跳入第二个activity
//        Toast.makeText(this, "camera Test", Toast.LENGTH_LONG).show();
//         第二個activity
        Intent intent = new Intent();
        intent.setClass(MainActivity.this,second.class);
        startActivity(intent);
    }



    /*
     * 调用摄像头，扫描二维码，模拟扫码，跳转伪装界面。
     *
     */


    public void getcode() {

        // xian # diao
        Intent intent = new Intent(MainActivity.this, CaptureActivity.class);
        startActivityForResult(intent, Constant.REQ_QR_CODE);

        }


        // 第二個activity
//        Intent intent = new Intent();
//        intent.setClass(MainActivity.this,secondActivity.class);
//        startActivity(intent);
//    }


    /**
     * 實現 頁面 動態變化功能
     */
    void startFlick() {
        ImageView s = findViewById(R.id.imageView);
        Animation alphaAnimation = new AlphaAnimation(1, 0.4f);
        alphaAnimation.setDuration(300);
        alphaAnimation.setInterpolator(new LinearInterpolator());
        alphaAnimation.setRepeatCount(Animation.INFINITE);
        alphaAnimation.setRepeatMode(Animation.REVERSE);
        s.startAnimation(alphaAnimation);

    }
}