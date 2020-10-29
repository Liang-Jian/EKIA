package com.wndk;

import androidx.appcompat.app.AppCompatActivity;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowManager;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;

import static android.view.View.SYSTEM_UI_FLAG_HIDE_NAVIGATION;
import static android.view.View.getDefaultSize;


/**
 *
 *  新建res 目录，读取res 目录。播放视频
 *
 *
 *
 */
public class second extends AppCompatActivity {
    VideoView mVideoView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);//去除标题栏
        setContentView(R.layout.activity_second);


        VideoView video = findViewById(R.id.videoView);
        MediaController md = new MediaController(second.this);
        video.setMediaController(md);
        video.setVideoURI(Uri.parse("android.resource://com.wndk/" + R.raw.faker));
        video.requestFocus();

        try{
            video.start();
        }catch (Exception e){
//            e.printStackTrace();
            ;
        }
        video.setOnCompletionListener(new MediaPlayer.OnCompletionListener(){
            @Override
            public void onCompletion(MediaPlayer mp){
                Toast.makeText(second.this, "视频播放完毕！", Toast.LENGTH_SHORT).show();
                finish();
            }
        });
    }

//    @Override
//    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
//        // TODO Auto-generated method stub
//
//        int width = getDefaultSize(0, widthMeasureSpec);
//        int height = getDefaultSize(0, heightMeasureSpec);
//        setMeasuredDimension(width, height);
//    }
}
