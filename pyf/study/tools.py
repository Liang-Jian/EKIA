import os
import re

__all__ =["get_target_value","Fuckyou"]
'''

import win32api
import win32con
#only windows system
def jeitu():
	win32api.keybd_event(44,0,0,0)
	win32api.keybd_event(44,0,win32con.KEYEVENTF_KEYUP,0)
	from PIL import ImageGrab
	im = ImageGrab.grabclipboard()
	im.save("a.BMP")
	im.show()


s = b'\xb1\xb1\xbe\xa9'
# print(s.decode('gb2312'))
# print(len(s))


class a:
    a = 'w32'

    def __init__(self):
        print('as')
    def test(self):
        print(a.a)
# if __name__ == '__main__':
#     a().test()



import array

# a = '234234'
# b= array.array('b',a)
# print('as array',b)

import weakref,scipy

import array,collections

a = array.array("B",range(3))
# print(a)
'''
import sys
te ={"data":{"carInfoVo":{"enrollDate":"2018-06-02","engineNo":"ASDF1234","carModel":[{"series":"甲壳虫BEETLE","importFlag":"进口","vehicleJingyou":{"fullWeightMax":"0","factoryName":"德国大众汽车股份公司","syxClassId":"KA","remark":"双离合 时尚型 涡轮增压","familyName":"甲壳虫BEETLE","vehicleHyName":"甲壳虫BEETLE 1.2TSI 时尚型","syxClassName":"六座以下客车","brandName":"大众","hfName":"正常","hfCode":"0","powerTypeCode":"D1","seat":"4","brandCode":"DZA0","vehicleHyCode":"BDZAJLUB0004","displacement":"1.197","kindredPriceTax":0,"seatMin":"4","power":"77","vehicleAlias":"","fullWeightMin":"0","importFlag":"进口","searchCode":"JKC-1.2TSI","familyCode":"DZA0AS","taxPrice":170800,"importFlagCode":"2","jqxClassName":"六座以下客车","fullWeight":"1307","price":"163800.0","vehicleName":"甲壳虫BEETLE 1.2TSI轿车","powerType":"汽油","vehicleClassName":"轿车类","marketDate":"201209","vehicleCode":"DZAASI0016","factoryCode":"MK0145","tonnage":"0.00","kindredPrice":0,"seatMax":"4","jqxClassId":"KA","vehicleClassCode":"IC01"},"modelCode":"DZAASI0016","riskFlag":"","industryModelName":"甲壳虫BEETLE 1.2TSI 时尚型","brandCN":"大众","vehicleWeight":1307.0,"alarmFlag":"","replacementValue":163800.0,"industryModelCode":"BDZAJLUB0004","modelName":"甲壳虫BEETLE 1.2TSI轿车","ratedPassengerCapacity":4.0,"displacement":1197.0,"airbagNum":0.0,"powerType":"0","tonnage":0.0,"marketYear":"201209"}],"vinNo":"21298234329U23432"},"responseFlag":"2"},"status":"1"}



'''
def li(dict_a,val_):

    if isinstance(dict_a,dict):
        for x in range(len(dict_a)):
            temp_key = list(dict_a.keys())[x]
            temp_val = dict_a[temp_key]

            if val_ == temp_key:
                print(temp_val)
                print(type(temp_val))
            # print ("%s:%s" % (temp_key,temp_val))
            # print(type(temp_key),type(temp_val))
            # print(temp_val)
            elif val_ != temp_key:
                li(temp_val, val_)
'''

'''遍历多层dict里面需要的值'''
'''
def dict_get(dict_, objkey, default=None):
    tmp = dict_
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            # if type(v) is types.Dict:
            if isinstance(v,dict):
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default
# print(dict_get(te,"carModel"))


def gre(names):
    for name in names:
        msg = 'hello' + name.title() + "*"
        namess = names.pop()
        print(namess)
dic = ['qq','xx','dd','ff','qq','ee']
'''

'''
from time import  sleep
n = 0
while n < 10:
    n +=1
    print(n)
    sleep(0.5)
    if n > 5:
        print('su')
        break
    else:
        continue
else:
    print('fuck')
'''

status  = True
while status:
    for i in range(3,19):
        print(i)
        if i == 14:
            print('find data')
            status = False
            break

    else:
        print('next page')

n=0
sta = False
for i in range(1,20):
    for k in range(1,20):
        n +=1
        print(n)
        if n==15:
            sta = True
            break
    if sta:
        break


import json
inp_strr = '{"k1":123, "k2": "456", "k3":"ares"}'
inp_dict = json.loads(inp_strr) # 根据字符串书写格式，将字符串自动转换成 字典类型
print (inp_dict)
print (type(inp_dict))

inp_dict.pop('k1')

print(inp_dict)


def dict_get(dict_, objkey, default=None):
    tmp = dict_
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            # if type(v) is types.Dict:
            if isinstance(v,dict):
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default




#这个最新的功能
def get_target_value(key, dic, tmp_list):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    else:
        for value in dic.values():  # 传入数据不符合则对其value值进行遍历
            if isinstance(value, dict):
                get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list


def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身




def getfile():
    _str = ""

    with open("file.txt","r",encoding="utf-8") as f:
        _str = "".join(f.readlines())
    print(_str.replace(" ",""))
    return _str


class Fuckyou(object):
    pass
# print(get_target_value("factorType",eval(getfile()),[]))
print(dict_get(te,"carModel"))


tel = "sfdsaffds33333-234"
s = re.findall("(\d+|\W\d+)",tel)
print(s)




from PIL import ImageGrab
import win32api
import win32con

# def jietu():
#     win32api.keybd_event(44,0,0,0)
#     win32api.keybd_event(44,0,win32con.KEYEVENTF_KEYUP,0)
#
#
#     im = ImageGrab.grabclipboard()
#     if isinstance(im,image.Image):
#         print(im.format,im.size,im.mode)
#         width,height =im.size
#         pix = im.load()
#         for x in range(width):
#             for y in range(height):
#                 print(pix[x,y])
#     else:
#         pass

# import inspect
# def get_current_():
#     return inspect.stack()[1][3]
# class fuck:
#     def dick(self):
#         print(get_current_())
#         print("%s.%s invoked" %  (self.__class__.__name__,get_current_()))
#         print(self.__class__.__name__)
# fuck().dick()























