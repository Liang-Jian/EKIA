package seleniumutils;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import org.apache.http.HttpStatus;
import org.apache.http.util.EntityUtils;
import org.testng.annotations.Test;

class AutoSelenium{
    private String driverpath = "/Users/jettech/Downloads/chromedriver" ;
    private String URL = "https://www.baidu.com";


    void loginMethod(){

        System.setProperty("webdriver.chrome.driver",driverpath);
        ChromeOptions options = new ChromeOptions();
        options.addArguments("disable-infobars");

        WebDriver dr = new ChromeDriver(options);
        dr.manage().window().maximize();
        dr.get(URL);

        try {
            Thread.sleep(1000);
        }catch (Exception e ) {e.printStackTrace();}
        dr.findElement(By.cssSelector("#kw")).sendKeys("fuck world");

    }

    public static void main(String[] args) {
        AutoSelenium s = new AutoSelenium();
        s.loginMethod();
    }

}



class Gener<T>{
    private  T  key;
    public Gener(T key){
        this.key = key;
    }

    public T getKey(){
        return key;
    }



}
