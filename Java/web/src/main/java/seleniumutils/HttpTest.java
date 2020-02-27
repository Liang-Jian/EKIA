package seleniumutils;


import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import com.alibaba.fastjson.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;


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

    public String dopost(String url){

        HashMap<String,String> test = new HashMap<>();
        test.put("","");
        test.put("","");
        HttpPost httpPost = new HttpPost(url);

//        httpPost.setHeader();
        return "s";
    }

    public static String URLPost(String url,Map<String,String> map) throws IOException {

        String str = JSONObject.toJSONString(map);
        String result = "";
        System.out.println("发送给对端的json串为："+str);
        DefaultHttpClient httpClient = new DefaultHttpClient();
        HttpPost httpPost = new HttpPost(url);
        // 设置请求的header
        httpPost.addHeader("Content-Type", "application/json;charset=utf-8");
        StringEntity entity = new StringEntity(str, "utf-8");
        entity.setContentEncoding("UTF-8");
        httpPost.setEntity(entity);

        HttpResponse response = httpClient.execute(httpPost);
        result = EntityUtils.toString(response.getEntity(), "utf-8");
        return result;
    }

    public static void main(String[] args) {
        HttpTest.doget("http://www.baidu.com");
    }
}
