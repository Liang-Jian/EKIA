package com.e.change;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class second extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

/*
        TextView textView = findViewById(R.id.textView2);
        Intent intent = getIntent();
        String tv = intent.getStringExtra("name");
        textView.setText(tv);*/
        TextView textView = findViewById(R.id.textView2);
        final Intent intent =getIntent();
        Bundle bundle = intent.getExtras();
        String tv = bundle.getString("name");
        textView.setText(tv);


        Button b1 = findViewById(R.id.button2);
        b1.setOnClickListener(new View.OnClickListener() {
/*            @Override
            public void onClick(View v) {
                EditText sexET =  findViewById(R.id.sex);
                String sex=sexET.getText().toString();
                Intent intent1=new Intent(second.this,MainActivity.class);
                intent1.putExtra("sex",sex);
                setResult(RESULT_OK,intent1);
                finish();
            }*/
            @Override
            public void onClick(View v){
                EditText sexET =  findViewById(R.id.sex);

                String sex=sexET.getText().toString();
                Log.i("sex",sex);
                Intent intent1=new Intent(second.this,MainActivity.class);
                Bundle bundle1 = new Bundle();
                bundle1.putString("sex",sex);
//                intent1.putExtra("sex",sex);
                intent1.putExtras(bundle1);
                setResult(RESULT_OK,intent1);
                startActivity(intent1);
                finish();
//                startActivityForResult(intent1,1989);
            }
        });
    }
}
