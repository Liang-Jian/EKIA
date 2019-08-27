package com.example.robot.ceshi;

/*import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedTest {
    @Test
    public void useAppContext() {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();
        assertEquals("com.example.robot.ceshi", appContext.getPackageName());
    }
}*/

import android.os.Bundle;
import android.support.test.InstrumentationRegistry;
import android.support.test.uiautomator.UiDevice;
import android.support.test.uiautomator.UiObject;
import android.support.test.uiautomator.UiObjectNotFoundException;
import android.support.test.uiautomator.UiSelector;
import android.util.Log;

import org.junit.Test;

import static android.support.test.InstrumentationRegistry.getArguments;

public class ExampleInstrumentedTest{

    private UiDevice uiDevice = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());
    //获取参数
    Bundle bundle = getArguments();
    private int displayWidth = uiDevice.getDisplayWidth();
    private int displayHeight = uiDevice.getDisplayHeight();

    @Test
    public void test() throws InterruptedException, UiObjectNotFoundException {
        uiDevice.pressHome();
        Log.i("test1", "在等待1111111111111");
        uiDevice.swipe(displayWidth / 2, displayHeight / 2, 0, displayHeight / 2, 10);
        while (true) {
            UiObject objectA = uiDevice.findObject(new UiSelector().text("华为钱包"));
            Thread.sleep(1000);
            if (objectA.exists()) {
                Thread.sleep(1000);
//                objectA.click();
//                Thread.sleep(1000);
                uiDevice.pressHome();
//                ShellRunner.shell("curl -d \"123\" http://192.168.51.225:8000/ud");
                Thread.sleep(1000);
            }
        }
    }
}
