import matplotlib.pyplot as plt
import  numpy as np
import random

#
# h = list()
# w = list()
# for i in range(10000):
#     h.append(random.randint(153,190))
#     w.append(random.uniform(51,88))
# print(w)
# print(h)

# age = np.array([13,19,22,14,19,11])
# print(age[-1])
# print(age[:3])
# print(age[:3])
# print(age[[0,3,5]])
# print(age[age < 18])
##################
# h = [1,2,3,4]
# s = [2,3,4,5]
# k = np.greater(h,s)
# k = np.greater_equal(h,s)
# k = np.less(h,s)
# k = np.less_equal(h,s)
# k = np.equal(h,s)
# print(k)
##################################
# r = np.random.uniform(0,1,1500)
# # print(r)
# initial =1000
# packages = [initial]
# for i in r:
#     # print(i,end='\n')
#     if i < 0.5:
#         initial -=8
#     else:
#         initial +=8
#     packages.append(initial)
# # print(initial)
# print(packages)
# plt.plot(range(1501),packages)
# plt.show()


######################################
import pandas as pd

# data1 = pd.read_csv('/Users/lexue/EKIA/python/spierfb/123.txt',skiprows=2,sep='')
# data1 = pd.read_csv('/Users/lexue/EKIA/python/spierfb/123.txt',skiprows=1,sep='',skipfooter=1,encoding='utf-8',names=['id','name','incom'])
data2 = pd.read_sql()

print(data2)
