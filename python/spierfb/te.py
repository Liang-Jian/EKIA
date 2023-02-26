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

s = ['湘南','Ｇ大阪']

def fixlist(ss):
    l = []
    for i in ss:
        # print(i)
        ee = ''
        for e in i:
            print(e)
            ee += f'{e}\n'
        l.append(ee)
    # print(l)
    return l
fixlist(s)