# share data  use queue
import queue,threading
# q = queue.Queue()
# q = queue.LifoQueue()
# for i in range(10):
#     prioritaet = i % 3
#     q.put((prioritaet,i))
# for i in range(10):
#     print(q.get())

#################
#
# q = queue.Queue()
# num_worker =4
# def do_work(item):
#     print(item)
# def worker():
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         do_work(item)
#         q.task_done()
# threads = []
# for i in range(num_worker):
#     t = threading.Thread(target=worker)
#     t.start()
#     threads.append(t)
# for i in range(100):
#     q.put(i)
# for i in range(num_worker):
#     q.put(None)
# for i in threads:
#     i.join()
#############################
# import multiprocessing,queue
# def calc_squre(numbers,q):
#     for n in numbers:
#         q.put(n*n)
# if __name__ == '__main__':
#     numbers = [2,3,5]
#     q = multiprocessing.Queue()
#     p = multiprocessing.Process(target=calc_squre,args=(numbers,q))
#     p.start()
#     p.join()
#     while q.empty() is False:
#         print(q.get())
#######################


# plt 做饼图
import matplotlib.pyplot as plt
# plt.rcParams['font.sans.serif']=['SimHei']
# edu = [0.25,0.35,0.1,0.3]
# labers = ['本科生','初中生','小学生','大专生']
# plt.pie(x=edu,labels=labers,autopct='%.1f%%')
# plt.show()


######################
# data1 = [1,4,2,6]
# data2 = ['a','b','c','d']
#
# plt.bar(x=range(1,6),height=5,tick_label='fuck',color='steelblue')
# plt.ylabel('gdp wanyi')
# plt.title('all flow data')
# for x,y in enumerate(data1.__dict__):
#     plt.text(x,y + 0.1, '%s' % round(y,1),ha='center')
# plt.show()



#####################
data1 = ['1','2','3','5']
data2 = ['3','12','14','5']
plt.plot(data1,
         data2.__len__(),
         linestyle='-',
         linewidth=2,
         color='steelblue',
         market='o',
         markersize=6,
         markeredgecolor='black',
         marketfacecolor='brown')
plt.ylabel='people count'
plt.title='every round conner count'
plt.show()