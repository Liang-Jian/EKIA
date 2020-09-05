package com.example.lexue;

import android.content.Context;
//import androidx.test.core.app.ApplicationProvider;

import org.junit.Test;

//import static com.google.common.truth.Truth.assertThat;
import android.content.Context;

import androidx.test.core.app.ApplicationProvider;
import androidx.test.filters.SdkSuppress;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.runner.AndroidJUnit4;
import androidx.test.runner.AndroidJUnitRunner;
//import androidx.test.ext.junit.runners.AndroidJUnit4;
//import org.robolectric.annotation.AccessibilityChecks;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;
public class UnitTestSampleJava {
    private static final String FAKE_STRING = "HELLO_WORLD";
    private Context context = ApplicationProvider.getApplicationContext();

    @Test
    public void readStringFromContext_LocalizedString() {
        // Given a Context object retrieved from Robolectric...
//        ClassUnderTest myObjectUnderTest = new ClassUnderTest(context);
//
//        // ...when the string is returned from the object under test...
//        String result = myObjectUnderTest.getHelloWorldString();
//
//        // ...then the result should be the expected one.
//        assertThat(result).isEqualTo(FAKE_STRING);
    }
}
