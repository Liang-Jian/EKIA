package com.example.lexue;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import androidx.test.espresso.web.webdriver.Locator;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;
import androidx.test.rule.ActivityTestRule;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.intent.Intents.intending;
import static androidx.test.espresso.intent.matcher.IntentMatchers.toPackage;
import static androidx.test.espresso.matcher.ViewMatchers.hasSibling;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static androidx.test.espresso.web.sugar.Web.onWebView;
import static androidx.test.espresso.web.webdriver.DriverAtoms.findElement;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.*;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.core.AllOf.allOf;

@RunWith(AndroidJUnit4.class)
@LargeTest
public class ChangeTextBehaviorTest {

    private String stringToBetyped;

    @Rule
    public ActivityTestRule<MainActivity> activityRule = new ActivityTestRule<>(MainActivity.class);


    @Before
    public void initValidString() {
        // Specify a valid string.
        stringToBetyped = "Espresso";
    }

    @Test
    public void changeText_sameActivity() {
        onView(withId(R.id.dick)).perform(click());
        onView(withId(R.id.dick)).check((matches(isDisplayed())));
        onView(withId(R.id.dick));
        onView(allOf(withText("7"), hasSibling(withText("item: 0")))).perform(click());

//        // Check that the text was changed.
//        onView(withId(R.id.textToBeChanged)).check(matches(withText(stringToBetyped)));

    }


    @Test
    public void webdriver_test(){
        // 测试与webview 交互
        onWebView().withElement(findElement(Locator.ID, "testID"));
        hasEntry(equalTo("STR"), is("item: 50"));
    }


//    @Rule
//    public IntentsTestRule<MyActivity> intentsTestRule = new IntentsTestRule<>(MyActivity.class);
//
//    @Test
//    public void intent_test(){
//        assertThat(intent).hasAction(Intent.ACTION_VIEW);
//        assertThat(intent).categories().containsExactly(Intent.CATEGORY_BROWSABLE);
//        assertThat(intent).hasData(Uri.parse("www.google.com"));
//        assertThat(intent).extras().containsKey("key1");
//        assertThat(intent).extras().string("key1").isEqualTo("value1");
//        assertThat(intent).extras().containsKey("key2");
//        assertThat(intent).extras().string("key2").isEqualTo("value2");
//    }


//    @Test
//    public void validateIntentSentToPackage() {
//        // User action that results in an external "phone" activity being launched.
//        user.clickOnView(system.getView(R.id.dick));
//
//        // Using a canned RecordedIntentMatcher to validate that an intent resolving
//        // to the "phone" activity has been sent.
//        intended(toPackage("com.android.phone"));
//    }


//    @Test
//    public void intent_test(){
//        Intent resultData = new Intent();
//        String phoneNumber = "123-345-6789";
//        resultData.putExtra("phone", phoneNumber);
//        Instrumentation.ActivityResult result = new Instrumentation.ActivityResult(Activity.RESULT_OK, resultData);
//
//    }


    @Test
    public void activityResult_DisplaysContactsPhoneNumber() {
        // Build the result to return when the activity is launched.
        Intent resultData = new Intent();
        String phoneNumber = "13613552859";
        resultData.putExtra("phone", phoneNumber);
        Instrumentation.ActivityResult result = new Instrumentation.ActivityResult(Activity.RESULT_OK, resultData);

        // Set up result stubbing when an intent sent to "contacts" is seen.
        intending(toPackage("com.android.contacts")).respondWith(result);

        // User action that results in "contacts" activity being launched.
        // Launching activity expects phoneNumber to be returned and displayed.
        onView(withId(R.id.dick)).perform(click());

        // Assert that the data we set up above is shown.
        onView(withId(R.id.dick)).check(matches(withText(phoneNumber)));
    }


}