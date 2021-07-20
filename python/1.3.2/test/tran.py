# -*- coding:utf-8 -*-
import threading,sys
from Queue import Queue
 
#假设有10000个任务
myqueue = Queue(10000)
for i in range(10000):
    myqueue.put('task%d' % (i + 1))
 
'''
任务执行方法，任务执行完成就被移除
以下只是简单输出任务执行字符串，并记录日志
'''
def foo():
    try:
        task = myqueue.get_nowait()
    except Exception, e:
        pass
    print '%s execute!' % task
 
    logfile = open('./log.txt', 'a')
    print >> logfile, '%s finish!' % task
    logfile.close()
 
#自定义线程类，继承threading.Thread
class MyThread(threading.Thread):
    def __init__(self, func, args=(), name=''):
        super(MyThread, self).__init__(target=func, args=args, name=name)
        self.name = name
        self.func = func
        self.args = args
 
    '''
    重写threading.Thread的run方法
    在这个方法中，会循环检测myqueue是否还有任务
    '''
    def run(self):
        while myqueue.qsize() > 0:
            self.func()
 
#主方法
def main():
    #开启30条线程来执行
    threads = []
    nloops = range(30)
 
    for i in nloops:
        t = MyThread(foo)
        threads.append(t)
 
    for i in nloops:
        threads[i].start()
 
    for i in nloops:
        threads[i].join()
 
if __name__ == '__main__':
    main()