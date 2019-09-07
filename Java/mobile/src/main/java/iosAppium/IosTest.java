package iosAppium;


import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.Assert;
import org.testng.annotations.*;

import java.net.MalformedURLException;
import java.net.URL;

public class IosTest {

    private static final String JavascriptExecutor = null;
    private static String URL = "http://0.0.0.0:4723/wd/hub";
    public WebDriver driver = null;


    void login() throws MalformedURLException { // open browser ,but  can't input url
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
