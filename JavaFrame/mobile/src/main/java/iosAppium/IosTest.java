package iosAppium;


import io.appium.java_client.MobileBy;
import io.appium.java_client.ios.IOSDriver;
import io.appium.java_client.ios.IOSElement;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;
import org.openqa.selenium.WebDriver;

import java.net.MalformedURLException;
import java.net.URL;

public class IosTest {

    private static final String JavascriptExecutor = null;
    private static String URL = "http://0.0.0.0:4723/wd/hub";
    public WebDriver driver = null;


    void login() throws MalformedURLException {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "iPhone X");
        capabilities.setCapability("platformVersion","11.3");
        capabilities.setCapability("platformName","iOS");
        capabilities.setCapability("browserName", "safari");
        driver = new RemoteWebDriver(new URL(URL), capabilities);
        System.out.println("app lunch");
        driver.get("https://m.baidu.com");


    }


    void login1() throws MalformedURLException {
        DesiredCapabilities capabilities = new DesiredCapabilities();
        capabilities.setCapability("deviceName", "iPhone X");
        capabilities.setCapability("platformVersion","11.3");
        capabilities.setCapability("platformName","iOS");
        capabilities.setCapability("browserName", "safari");
        driver = new RemoteWebDriver(new URL(URL), capabilities);
        System.out.println("app lunch");

        driver.get("http://appium.io/");
        Assert.assertEquals(driver.getCurrentUrl(), "http://appium.io/", "URL Mismatch");
        Assert.assertEquals(driver.getTitle(), "Appium: Mobile App Automation Made Awesome.", "Title Mismatch");

    }


    public static void main(String[] args) {
        try {
            IosTest io = new IosTest();
            io.login1();
        } catch (Exception e) {;}
    }
}
