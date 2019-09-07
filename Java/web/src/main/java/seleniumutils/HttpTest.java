package seleniumutils;


import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;


public class HttpTest {

     static String doget(String url){
        try{
            HttpClient client = new DefaultHttpClient();
            HttpGet request = new HttpGet(url);

//            request.setHeader(new BasicHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"));
//            request.setHeader(new BasicHeader("Accept", "text/plain;charset=utf-8"));
            HttpResponse respon = client.execute(request);

            if (respon.getStatusLine().getStatusCode() == HttpStatus.SC_OK){
                String strresult =EntityUtils.toString(respon.getEntity(),"utf-8");
                System.out.println(strresult);
                return strresult;
            }
        }
        catch (Exception e ) {
            e.printStackTrace();
        }
        return null;

    }


    private boolean isRight(){
        return false;
    }
    static int dopost(){
        return 1;
    }


    public static void main(String[] args) {
        HttpTest.doget("http://www.baidu.com");
    }
}
