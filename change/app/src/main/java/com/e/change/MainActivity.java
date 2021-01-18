package com.e.change;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button b = findViewById(R.id.button);
        b.setOnClickListener(new View.OnClickListener() {
/*            @Override
            public void onClick(View v) {
                Intent  intent = new Intent(MainActivity.this,second.class);
                EditText editText = findViewById(R.id.editText);
                String name = editText.getText().toString();
                intent.putExtra("name",name);
//                startActivity(intent);
                startActivityForResult(intent,1);
            }*/
            @Override
            public void onClick(View v) {
                Intent  intent = new Intent(MainActivity.this,second.class);
                EditText editText = findViewById(R.id.editText);
                String name = editText.getText().toString();

                Bundle bundle= new Bundle();
                bundle.putString("name",name);
                intent.putExtras(bundle);
                startActivityForResult(intent,1);
//                startActivity(intent);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
/*        switch (requestCode) {
            case 1:
                if (resultCode == RESULT_OK) {
                    String retinfo = data.getStringExtra("sex");
                    TextView textView1 = findViewById(R.id.textView);
                    textView1.setText(retinfo);
                    //Log.d(TAG,retinfo);
                }
                break;
            default:
        }*/
/*
        if(requestCode == 0 && resultCode == 0){
            Bundle data = intent.getExtras();
            System.out.println(data.getString("test4"));
        }*/
//        if (requestCode==RESULT_OK){
////            if (resultCode==ResultActivity.ResultCode){
//                Bundle bundle = data.getExtras();
//                String result = bundle.getString("sex");//通过key值进行获取返回的参数
//            TextView textView1 = findViewById(R.id.textView);
//            textView1.setText(result);
////            }
//        }

//        switch (requestCode) {
//            case 1:
//                if (resultCode == RESULT_OK) {
//                    Bundle bundle = data.getExtras();
//                    String result = bundle.getString("sex");
//                    TextView textView1 = findViewById(R.id.textView);
//                    textView1.setText(result);
//                    //Log.d(TAG,retinfo);
//                }
//                break;
//            default:
//        }
//        Intent intent = getIntent();
        Bundle bundle = data.getExtras();
////        String fs = bundle.getString("sex");
////        System.out.println(fs);
//
//        Log.d("TAG","newPwd"+ data.getExtras().getString("sex"));
//        System.out.println(requestCode);
//        System.out.println(resultCode);
//        Toast.makeText(MainActivity.this,data.getExtras().getString("sex"),Toast.LENGTH_LONG).show();
    }
}
