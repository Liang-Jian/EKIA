package com.example.joker.android;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.WindowManager.LayoutParams;
import android.widget.Toast;

//

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.getWindow().addFlags(LayoutParams.FLAG_SECURE);  // 禁止截屏

        try {Thread.sleep(3000);} catch (Exception e) {}

        Toast.makeText(this, "Fuck This World", Toast.LENGTH_SHORT).show();

    }



}
