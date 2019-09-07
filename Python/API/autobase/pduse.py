
import json
# import pandas as pd
import collections


'''
.ix is deprecated. Please use
.loc for label based indexing or
.iloc for positional indexing
'''
#
# df=pd.read_excel('/home/robot/ApiTestFrame/autodata/testcase/小渠道一步希望.xlsx',sheet_name='核保出单')#可以通过sheet_name来指定读取的表单
# data=df.head(100)#默认读取前5行的数据
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# print("获取到所有的值:\n{0}".format(data))#格式化输出
#
# print("====")
'''
#1：读取指定行
# df=pd.read_excel('记账系统用例及数据-UAT2.xlsx')#这个会直接默认读取到这个Excel的第一个表单
data=df.iloc[0].values#0表示第一行 这里读取数据并不包含表头，要注意哦！
print("读取指定行的数据：\n{0}".format(data))


# df=pd.read_excel('记账系统用例及数据-UAT2.xlsx')
data=df.iloc[[0]].values#读取指定多行的话，就要在ix[]里面嵌套列表指定行数
print("读取指定行的数据：\n{0}".format(data))

#读取指定的行列
# df=pd.read_excel('记账系统用例及数据-UAT2.xlsx')
# data=df.ix[1,2]#读取第一行第二列的值，这里不需要嵌套列表
data=df.iloc[0,0]#读取第一行第二列的值，这里不需要嵌套列表
print("读取指定行列的数据：\n{0}".format(data))

#读取指定的多行多列值
data=df.loc[[1,2],['name','sex']].values#读取第一行第二行的title以及data列的值，这里需要嵌套列表
print("读取指定多行多列值的数据：\n{0}".format(data))


#获取所有行的指定列
# data=df.ix[:,['age','sex']].values#读所有行的title以及data列的值，这里需要嵌套列表
data=df.loc[:,['name','age']].values#读所有行的title以及data列的值，这里需要嵌套列表
print("读取指定列的数据：\n{0}".format(data))
print(type(data[0][0]))
#6：获取行号并打印输出
print("输出行号列表",df.index.values)


#7：获取列名并打印输出
print("输出列标题",df.columns.values)


#8：获取指定行数的值：
print("输出值",df.sample(3).values)#这个方法类似于head()方法以及df.values方法

#9：获取指定列的值：
print("输出值\n",df['name'].values)


test_data=[]
test_dict=collections.OrderedDict()
for i in df.index.values:#获取行号的索引，并对其进行遍历：行号
    #根据i来获取每一行指定的数据 并利用to_dict转成字典
    row_data=df.loc[i,['name','age','sex']].to_dict()
    test_dict[i] = row_data
print("最终获取到的数据是：{0}".format(test_dict))
print(test_dict.get(2))
'''


# data=df.loc[:,['name','age']].values#读所有行的title以及data列的值，这里需要嵌套列表
# print("读取指定列的数据：\n{0}".format(data))
# print(type(data[0][0]))
# #6：获取行号并打印输出
# print("输出行号列表",df.index.values)


# dick = dict()
# for k in data:
#     dick.update({k[0]:k[1]})
# print(dick)



def a(*args,**kwargs):
    print(*args,**kwargs)

# a({'a':'df'})


k = {"a":"b","b":1}
k["a"]=3

print(k)





from kafka import KafkaProducer

producter = KafkaProducer(bootstrap_servers="10.10.85.237:9092")

msg_dict ={"IPCounty":"fuck","JnlDate":"kehuqing","MateMobilePhone":"kehuqing","GuarantorPhone":"kehuqing","businessId":"cdbc2cc3-fa02-4ef6-87e7-e783952c5215","WorkingEntName":"kehuqing","LiveAddr":"kehuqing","BankCard":"kehuqing","MobilePhone":"test4","NetWorkType":"kehuqing","IsProduction":"production","GPSAddr":"125*39","MateIdNo":"test","RecFaceFaildNum":1,"RecFaceTimePoints":"kehuqing","productId":"kehuqing","IPProvince":"kehuqing","IP":"kehuqing","BaseStationInfo":"kehuqing","ContactMobilePhone":"kehuqing","IPCity":"kehuqing","JnlNo":"95b85f9d-d1b3-4e55-9c72-8051d05c546a","MateEntName":"kehuqing","MaritalStatus":"marry12","BSSID":"kehuqing","WorkingTelephone":"kehuqing","idfvimei":"kehuqing","MACAddr":"kehuqing","JnlTimestamp":"2019-06-12 06:50:00.988","EduBackgroup":"kehuqing","IdNo":"f3e683","IdAddr":"test"}

msg = json.dumps(msg_dict)

producter.send("afdLoansApplyOnlineTopic",bytes(msg,encoding="utf-8"),partition=0)

producter.close()
print("success")




