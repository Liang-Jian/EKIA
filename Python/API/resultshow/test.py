
# li = list()
# for x in range(5):
#     li.append(lambda x: x**2)
#
# print(li[0](2)) # 4
# print(li[1](3)) # 9
# print(li[0](1))
#
#
#
# # y = list(filter([ lambda  :x for x in range(4)]))
#
# newlist = list(filter(lambda n:n%2==1,[1,2,3,4,5,6,7,8,9,10]))
#
# # print(y[0](2))
# print(newlist)
# # print(y)
#
# z = list(x for x in [1,2,3,4,5,6,7,8,9,10] if x%2==1)
# print(z)
#
# #map（函数,shuju）
# k = list(map(lambda x:x*2,[1,2,3,4,5]))
# print(k)
#
#
# def dick(a):
#     return a*2
# dd = list(map(dick,[1,2,3,4]))
# print(dd)
#
#
# def normalize(name):
#     print(name)
#     return name[0].upper()+ name[1:].lower()
# Name = ['lily','JACK','mAriN']
#
# s = (list(map(normalize,Name)))
# print(s)
#
#
# from functools import reduce
# def sum(x,y):
#     return x+y
# l = [1,2,3,4,5,6]
# l = reduce(sum,l)
# print(l)
#
# l = [1,2,3,4,5,6]
# l = reduce(lambda x,y:x+y,l)                # 结合lambda
# print(l)
# help(reduce)


# from openpyxl import load_workbook
#
# wb = load_workbook("/home/robot/ApiTestFrame/autodata/testcase/小渠道一步希望.xlsx")
#
#
# print(wb.sheetnames) #get danyuange
# asheet = wb.get_sheet_by_name("核保出单")
# a1 = asheet['A1']
# print(a1)


# for row in asheet.rows:
#     for cell in row:
#         print(cell.value)

# for col in asheet.columns:
#     for cell in col:
#         print(cell.value)
import queue
import time
import threading

# q = queue.Queue()
# def a():
#
#     for i in range(3):
#
#         print('a'+time.ctime())
#         time.sleep(1)
# def b():
#     for k in range(4):
#         print('b'+time.ctime())
#         time.sleep(2)
#
#
# t = list()
# t1 = threading.Thread(target=a,args=())
# t.append(t1)
# t2 = threading.Thread(target=b,args=())
# t.append(t2)
#
# for i in t:
#     i.setDaemon(True)#  true 父进程死，县城死
#     i.start()



###########################
# def a(num):
#     print("running thread: %s" % num)
#
# def b():
#     pass
#
# t = list()
# t1 = threading.Thread(target=a,args=("s",))
# t.append(t1)
# t2 = threading.Thread(target=b,args=())
# t.append(t2)
# for k in t:
#     k.start()
#     print(k.getName())
#
#
# class te(threading.Thread):
#     def __init__(self,num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#
#     def run(self):
#         print("running thread %s " % self.num)
#         time.sleep(3)
#
# if __name__ == '__main__':
#     t1 = te(1)
#     t2 = te(2)
#     t1.start()
#     t2.start()

############################

# def addNum():
#     global num
#     print("-get num:",num)
#     time.sleep(1)
#     num -=1
#
# num = 100
# thread_list = list()
# for i in range(100):
#     t = threading.Thread(target=addNum)
#     t.start()
#     thread_list.append(t)
# for t in thread_list:
#     t.join()
#
# print("final num ",num)


###########################

