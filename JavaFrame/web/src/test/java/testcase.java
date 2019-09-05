import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import org.testng.Assert;

public class testcase {
    public int add(int i ,int j){
        int m;
        m = i + j;
        return m;

    }

    @BeforeClass
    void f() {
        System.out.println("bef");
    }

    @AfterClass
    void d(){
        System.out.println("aft");
    }
    @Test
    public void testadd(){
        if (2 == add(1, 1)) {
            System.out.println("pass");
        }else {
            System.out.println("fail");
        }
    }
}
