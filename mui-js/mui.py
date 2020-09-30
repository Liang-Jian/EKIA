

# from appium import webdriver



'''

1, 微信 这边需要开启debug模式  debugx5.qq.com
2,
'''

def a(ele,p_ele):
    _js = '''function joker(){ \
            var ele_list = mui('%s'); \
            for (var i=0;i<ele_list.length;i++){ \
                  if (q[i].innerText == '%s'){ \
		            q[i].addEventListener('tap',function(){}); \
		            mui.trigger(q[i],'tap');\
	            } \
            } \
        };joker();''' % ("h4","班级")
    print(_js)
a('a','b')