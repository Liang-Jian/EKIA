'''


移动端自动化经验:
    1,使用appium + webview
    2,原生app使用appcrawler


appcrawler  config

demo.yml : appcrawler 设置详情

# 生成 配置文件
D:\app-discovey>java -jar appcrawler-2.4.0-jar-with-dependencies.jar -c demo.yml

# 启动安装完成app
java  -jar appcrawler-2.4.0-jar-with-dependencies.jar --capability "appPackage=com.lexue.zhongkao,appActivity=com.lexue.courser.main.view.MainActivity" -c example.yml









'''