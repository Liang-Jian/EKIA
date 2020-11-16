
import urllib.parse
# values={}
# values['username']='02蔡彩虹'
# values['password']=[123,2334,234]
# print(values)
# url="http://www.baidu.com"
# data=urllib.parse.urlencode(values)
# print(data)

k= {"a":"c","b":[1,2,3]}

def tostr(any):
	if isinstance(any,int):
		any = str(any)
	elif isinstance(any,list):
		any = urllib.parse.urlencode(any)
	return any

