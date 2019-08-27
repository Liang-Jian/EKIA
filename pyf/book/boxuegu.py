

'''
class Tool(object):
    num = 0
    def __init__(self,new_name):
        self.name = new_name
        Tool.num +=1
tool1 = Tool("suck")
tool2 = Tool("dick")
tool3 = Tool("pussy")
print(Tool.num)
'''
import os
import time

'''
class Tool(object):
    def __init__(self,new_name):
        self.name = new_name
num = 0
tool1 = Tool("fuck")
num +=1
print(num)

tool2 = Tool("suck")
num +=1
tool3 = Tool("dick")

num +=1
print(num)



class Game(object):
    num = 0
    def __init__(self):
        self.name = "laowang"
    @classmethod
    def add_num(cls):
        cls.num = 100
    @staticmethod
    def print_num():
        print('==============')
        print("start ")
        print("gamin ")
        print("overd ")
        print('==============')
game = Game()
game.add_num()
print(game.num)
Game.print_num()
game.print_num()
'''

'''
class Store(object):
    def select_car(self):
        pass
    def order(self,car_type):
        return self.select_car(car_type)
class BMWcarstore(Store):
    def select_car(self):
        return BMW

class CarStore(object):
    def __init__(self):
        self.factor = SelectCar()
    def order(self,car_type):
        return self.factor.select_car_by_type(car_type)
class SelectCar(object):
    def select_car_by_type(car_type):
        if car_type == "lexus":
            return Lexus()
        elif car_type == "cadillac":
            return Cadillac()
        elif car_type == "benze":
            return Benze()
class Car(object):
    pass
    def move(self):
        print("car is move")
    def music(self):
        print("car is play")
    def stop(self):
        print("car is stop")
class Lexus(Car):
    pass
class Cadillac(Car):
    pass
class Benze(Car):
    pass
car_store = CarStore()
car = car_store.order("cadillac")
car.move()
car.music()
car.stop()


class Cat(object):
    def __init__(self):
        print('__init__')

    def __del__(self):
        print('__del__')
    def __str__(self):
        print('__str__')
    def __new__(cls, *args, **kwargs):
        print(id(cls))
        print('__new__')
        return object.__new__(cls)
print(id(Cat))
dt = Cat()

class Dog(object):
    # 所谓的单例模式 yoyoyo
    __instance = None
    __str = False
    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance
    def __init__(self,name):
        if Dog.__str is False:
            self.name =name
            Dog.__str = True
a = Dog("A")
print(id(a))
print(a.name)
b = Dog("B")
print(id(b))
print(b.name)
'''
'''
try:
    # open("a.txt",'r')
    # print(num)
    print('--1--')
except (NameError,FileNotFoundError):
    print("如果捕获到异常后")
except Exception as ret:
    print("不是上述两个yichang")
    print(ret)
else:
    print("没有异常出现情况")
finally:
    print("fin")
print('---2---')
'''
'''
class Test(object):
    def __init__(self,status):
        self.status = status
    def calc(self,a,b):
        try:
            return a/b
        except Exception as result:
            if self.status:
                print("zhua dao yichantg")
                print(result)
            else:
                pass
a = Test(True)
a.calc(11,0)
print('-----')
a.status = False
a.calc(11,0)

from bet.demo.get_key_ import *
k =Fuckyou()

a = [i for i in range(1,55)]
print(a)
b = [11 for i in range(1,18)]
print(b)
c = [i for i in range(10) if i%2 ==0]
print(c)
d = [i for i in range(3) for j in range(5)]
print(d)
e = [(i,j)for i  in range(3) for j in range(3)]
print(e)


k = [11,22,33,33,44]
sor_k = set(k)
kl = list(sor_k)
print(sorted(kl))

result =''
bySourceByte = b'\xfc\xa5\xc9\x16\x1eT\xa6\xe9\x1e\xc6\x07G\xec7\xaf\xb2'
len = len(bySourceByte)
for i in range(len):
    tb = bySourceByte[i]
    print(tb)
    tmp = chr(tb >> 4 & 0xF)
    print(tmp)
    if (tmp >= '\n'):
        high = chr(97 + ord(tmp) - 10)
        print(high)
    else:
        high = chr(ord('0') + ord(tmp))
        print(high)
    result += high
    tmp = chr(tb & 0xF)
    print('--------------'+tmp)
    if (tmp >= '\n'):
        low = chr(97 + ord(tmp) - 10)
        print(low)
    else:
        low = chr(ord('0') + ord(tmp))
        print(low)
    result += low

print(result)



def query(url):
    requests.get(url)

start = time.time()
for i in range(100):
    query("http://10.130.201.36:index.jsp")
end = time.time()
print('单线程访问100次百度首页，耗时:{}'.format(end-start))

start1 = time.time()
url_list = []
for i in range(10):
    url_list.append("http://*.*.*/index.jsp")
pspp = Pool(5)
pspp.map(query,url_list)
end1 = time.time()

print('多线程访问100次百度首页，耗时:{}'.format(end1-start1))

'''
'''
#模板因穷 str--> dick/json
def moban():
    f  = open("./demo.txt")
    file = f.read()
    print(repr(file))
    ks = {"dick":"big","fuck":"you","suck":"dick","duck":"me"}
    from jinja2 import Template
    # templete = Template("hell0 {{name}}")
    templete = Template(file)
    k = templete.render(ks)
    print(type(k))
    print(repr(k))
    # eval(k)
    import json
    ff = json.loads(k)
    print(type(ff))
    print(ff)
'''
'''
import threading
def hi(num):
    print("hello %d\n" % num)
    time.sleep(3)

if __name__ == '__main__':

    t1 = threading.Thread(target=hi,args=(3,)) #target传入函数名字 args为参数 ，此写法固定的
    t1.start()

    t2 = threading.Thread(target=hi,args=(4,))
    t2.start()
    print("ending...")


import threading

def music():
    print("begin list %s" % time.ctime())
    time.sleep(2)
    print("end list %s" % time.ctime())

def game():
    print("begin play %s" % time.ctime())
    time.sleep(3)
    print("end play %s" % time.ctime())

if __name__ == '__main__':
    t=threading.Thread(target=music)
    t1 = threading.Thread(target=game)
    t.start()

    t1.setDaemon(True)  #必须放在start之前，  true 意思是和主线程一起注销，主线成 退出，设为true的也会退出。不管是否运行完成
    t1.start()  # start 只是处于一个就绪的状态，并非执行的状态
    # t.join() #t 这个线程结束不结束谁也不许做下一步
    # t1.join()
    print(t.getName())
    print(threading.active_count())
    print("ending")
    # l = list()
    # for i in range(2):
    #     l.append(threading.Thread(target=music))

class Mythrea(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)

        self.name = name

    def run(self):
        pass

if __name__ == '__main__':
    t = Mythrea(1)
    t2= Mythrea(2)
    t.start()
    t2.start()
    print("sdfs")'''


import threading

# def foo():
#     print('ok')
#
#
# t1 = threading.Thread(target=foo)
# t1.start()

def add():
    sum = 1
    for i in range(1000):
        sum +=i
    print(sum)
def mul():
    sum2 =1
    for i in range(1,1000):
        sum2 *=i
    print(sum2)

# t1 =threading.Thread(target=add)
# t2 =threading.Thread(target=mul)
# start = time.time()
# print(start)
# thread = []
# thread.append(t1)
# thread.append(t2)

# for t in thread:
#     t.start()
# for t in thread:
#     t.join()
# end = time.time()
# print(end)
# add()
# mul()

'''
def sub():
    # global eum
    # time.sleep(0.1)
    # eum-=1

    global eum
    lock.acquire()
    temp = eum
    time.sleep(0.01)
    eum = temp -1
    lock.release()  #这个县城没完成钱不准切换cpu
eum = 100


lock = threading.Lock()
l = list()
for i in range(100):
    t = threading.Thread(target=sub)
    t.start()
    l.append(t)
for t in l:
    t.join()
print(eum)'''

'''
class Mythread(threading.Thread):

    #线程死锁 ，释放后才能
    def actionA(self):
        A.acquire()
        print(self.name,"goba", time.ctime()) #self.name 线程名字
        time.sleep(2)

        B.acquire()
        print(self.name, "gotb" ,time.ctime())
        time.sleep(1)
        B.release()
        A.release()
    def actionB(self):
        B.acquire()
        print(self.name, "gobB", time.ctime())  # self.name 线程名字
        time.sleep(2)

        A.acquire()
        print(self.name, "gota", time.ctime())
        time.sleep(1)
        A.release()
        B.release()


    def run(self):
        self.actionA()
        time.sleep(3) # 3s 和 2 s 不一样。拿到锁的时间
        self.actionB()

if __name__ == '__main__':

    A = threading.Lock()
    B = threading.Lock()
    L = list()
    for i in range(2):
        t = Mythread()
        t.start()
        L.append(t)

    for i in L:
        i.join()
    print("ending")
'''

#
# class Mythread(threading.Thread): #递归锁,维持一把锁。
#
#     #线程死锁 ，释放后才能
#     def actionA(self):
#         r_lock.acquire()
#         print(self.name,"goba", time.ctime()) #self.name 线程名字
#         time.sleep(2)
#
#         r_lock.acquire()
#         print(self.name, "gotb" ,time.ctime())
#         time.sleep(1)
#         r_lock.release()
#         r_lock.release()
#     def actionB(self):
#         r_lock.acquire()
#         print(self.name, "gobB", time.ctime())  # self.name 线程名字
#         time.sleep(2)
#
#         r_lock.acquire()
#         print(self.name, "gota", time.ctime())
#         time.sleep(1)
#         r_lock.release()
#         r_lock.release()
#
#
#     def run(self):
#         self.actionA()
#         time.sleep(1) # 3s 和 2 s 不一样。拿到锁的时间
#         self.actionB()
# if __name__ == '__main__':
#     r_lock = threading.RLock()
#
#
#     L = list()
#     for i in range(2):
#         t = Mythread()
#         t.start()
#         L.append(t)
#
#     for i in L:
#         i.join()
#     print("ending")

'''
class Mythear(threading.Thread): #信号量

    def run(self):
        if sem.acquire():
            print(self.name)
            time.sleep(3)
            sem.release()
if __name__ == '__main__':
    sem = threading.Semaphore(3) #每次线程分的数量 ,相当与同时有3把锁
    thr = list()
    for i in range(100):
        thr.append(Mythear())
    for t in thr:
        t.start()'''

''' 线程NO安全
l = [1,2,3,4,5]
def pr():
    while l:
        a =l[-1]
        print(a)
        time.sleep(1)
        l.remove(a)

t1 = threading.Thread(target=pr,args=())
t2 = threading.Thread(target=pr,args=())
t1.start()
t2.start()
'''

'''
import queue

q = queue.Queue(3)
q.put("he")
q.put("man")
q.put("man")
q.put("man",block=False)

while 1:
    daa = q.get()
    print(daa)
    print('====')
'''


import queue,random
# q =queue.Queue()
#
# def produce(name):
#     count = 1
#     while count < 10:
#         print("造包子")
#         time.sleep(random.randrange(5))
#         q.put(count)
#
#         print("produce %s procude %s baozi\r" % (name,count))
#         count +=1
#         q.task_done() #faru yige xinhao  join() && task-done一起配合使用
#         print("ok")
# def custome(name):
#     count = 1
#     while count <10:
#         time.sleep(random.randrange(4))
#         if not q.empty():
#             print("waiting")
#             # q.join()
#             data  = q.get()
#             q.join() #send xinhao
#             print(" consumer %s eat %s baozi\r" % (name,data))
#         else:
#             print("no baozi ")
#         count +=1
# p1 = threading.Thread(target=produce , args=("A君",))
# p2 = threading.Thread(target=custome , args=("B君",))
# p3 = threading.Thread(target=custome , args=("C君",))
# p4 = threading.Thread(target=custome , args=("D君",))
# p1.start()
# p2.start()
# p3.start()
# p4.start()


# from multiprocessing import Process
# def mp(name):
#     time.sleep(1)
#     print("hello %s at %s " % (name,time.ctime()))
# pp = list()
# for i in range(3):
#     p  = Process(target=mp,args=("fuck",))
#     # p.daemon=True
#     pp.append(p)
#     p.start()
# # for i in pp:   #you join he meiyou bu yiyang ..
# #     i.join()
# print("ok...")


# from multiprocessing import Process
# import os
# def info(title):
#     print("title %s" % title)
#     print("parent process :",os.getppid())
#     print("process " , os.getpid())
#
# def f(name):
#     info("function f")
#     print("hellow", name)
#
# # info("main process line")
# # time.sleep(1)
# # print("----")
# info("main process line")
# time.sleep(1)
# p = Process(target=info,args=("yuan",))
# p.start()
# p.join()


#i进程调用
from multiprocessing import Process
# class MyProces(Process):
#     def __init__(self,num):
#         # Process.__init__(self,)
#         super(MyProces,self).__init__()
#         self.num = num
#     def fuck(self):
#         print("fuck girl")
#     def run(self):
#         time.sleep(1)
#         print(self.pid)
#         print(self.is_alive())
#         # self.fuck()
#         print(self.name)
# def foo(i):
#     time.sleep(1)
#     print(p.is_alive(),i,p.pid)
#     time.sleep(1)
# # p_list = list()
# # for i in range(10):
# #     p = Process(target=foo,args=(i,))
# #     p_list.append(p)
# # for p in p_list:
# #     p.start()
# # print("main process end")
# pl = list()
# for i in range(10):
#     p = MyProces(i)
#     pl.append(p)
# for i in pl:
#     i.start()
#     # i.join()
# print("main process end")


# jincheng jian tongxin
# import queue
# import multiprocessing
# def foo(q):
#     time.sleep(1)
#     print("son",id(q))
#     q.put(123)
#     q.put("yuan")
#
# # q = queue.Queue()
# q = multiprocessing.Queue() #duo jincheng yong muti
# p = multiprocessing.Process(target=foo,args=(q,))
# p.start()
# # p.join()
# print("mainprocess",id(q))
# print()
# print(q.get())
# print(q.get())

from multiprocessing import Process,Pipe,Lock
#pip shuangxiang guandao

# def f(conn):
#     conn.send([12,{"name":"yuan"},"fuck"])
#     reponse = conn.recv()
#     print("respons",reponse)
#     conn.close()
#     print("q_id2",id(child_conn))
# patrent_conn,child_conn= Pipe()
# p = Process(target=f,args=(child_conn,))
# p.start()
# print(patrent_conn.recv())
# patrent_conn.send("heelow son")
# p.join()


# def f(l,i):#加上锁后就变成了串行的。
#     l.acquire()
#     time.sleep(1)
#     print("Fuck world",time.ctime())
#     l.release()
# lock = Lock()
# for i in range(10):
#     Process(target=f,args=(lock,i)).start()


# from multiprocessing import Pool
# #进程池
# def foo(i):
#     time.sleep(1)
#     print(i)
#     # return i + 100
# def bar(arg):
#     print(os.getpid() )
#     print(os.getppid())
#     print("logger",arg)
#
# p = Pool(5) #进程吃对象
# # bar(1)
# for i in range(100):
#     p.apply_async(func=foo,args=(i,),callback=bar)#,callback=bar 回调函数，值得是成功调用后又运行的函数.
#     # p.apply(func=foo,args=(i,),callback=bar)#,同步接收任务
# p.close() #join he close 同时用的时候顺序固定
# p.join()
# print("end")


#携程
# def f():
#     print("fuck")
#     yield  #用户太切换，，生称其对象
#     print("fuck me")
#     yield
# ggen =f()
# print(ggen)
# print(ggen.__next__())



#携程
# def consumer(name):
#     print("--->read to eat baozi..")
#     while True:
#         new_baozi = yield
#         print("%s eating baozi %s" % (name,new_baozi))
# def producer():
#     r = con.__next__()
#     r = con2.__next__()
#     n = 0
#     while n < 10:
#         time.sleep(1)
#         print("m is making baozi %s and %s " % (n,n+1))
#         con.send(n)
#         con2.send(n+1)
#         n+=2
# con = consumer("c1")
# con2 = consumer("c2")
# p=producer()


#携程 grand
# from greenlet import greenlet
# def test1():
#     print(12)
#     gr2.switch()
#     print(32)
#     gr2.switch()
#
# def test2():
#     print(34)
#     gr1.switch()
#     print(89)
#
# gr1 = greenlet(test1)
# gr2 = greenlet(test2)
# gr2.switch()


import requests ,time
def f(url):
    print("get",url)
    resp = requests.get(url)
    data = resp.text
    f = open("new","wb")
    f.write(data.encode("utf-8"))
    f.close()
start = time.time()
f("https://www.baidu.com")
print("cost tiem",time.time()-start)