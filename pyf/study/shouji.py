    from appium import webdriver
import time


class AndroidTest:
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '7.0'  # 手机系统版本
        desired_caps['deviceName'] = 'CB******'  # 刚才的devicename
        desired_caps['appPackage'] = 'com.android.calculator2'  # 计算器的package
        desired_caps['appActivity'] = 'com.android.calculator2.Calculator'  # 计算器的activity
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)  # 运行该脚本desired_caps

    def touch(self):
        time.sleep(3)
        print("connect successfullly")
        self.driver.find_element_by_android_uiautomator()
        self.quit()

    def quit(self):
        self.driver.quit()
if __name__ == '__main__':
    AndroidTest().touch()
