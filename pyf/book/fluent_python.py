

### <<流畅的python>> ###
'''
promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promos

@promotion
def
'''


b = 5
def fi(a):
    print(a)
    b =3
    print(b)
fi(3)

# from dis import dis  #查看字节码
# dis(fi(9))
##################################
def make_aver():
    series = []
    def averager(new_value):
        series.append(new_value)
        total = sum(series)

        print(total/len(series))
        return total/len(series)
    return averager

# eva = make_aver()
# eva(10)
# eva(11)


#############

def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count,total #变量标记为自由变量
        count += 1
        total += new_value
        return total / count
    return averager


###########
import time
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ','.join(repr(args) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed,name,arg_str,result))
        return result
    return  clocked

@clock
def snooze(seconds):
    time.sleep(seconds)
@clock
def factorial(n):
    return 1 if n < 2  else  n * factorial(n-1)
# print("* "* 40,'calling snooze(.123)')
# snooze(.123)
# print("* "* 40,'calling factor(6)')
# print('6 !=',factorial(6))


################
import functools,time

# def clock(func):
#     @functools.wraps(func)
#     def clocked(*args,**kwargs):
#         t0 = time.time()
#         elapsed = time.time() - t0
#         result = func(*args,**kwargs)
#         name = func.__name__
#         arg_list = []
#         if args:
#             arg_list.append(','.join(repr(arg) for arg in arg_list))
#         if kwargs:
#             pairs = ['%s=%r' % (k,w) for k,w in sorted(kwargs.items())]
#             arg_list.append(', '.join(pairs))
#         arg_str = ','.join(arg_list)
#         print('[%0.8fs] %s(%s) -> %r ' % (elapsed,name,arg_str,result))
#         return result
#     return clocked
#
# @clock
# def fibonacci(n):
#     if n < 2:
#         return n
#     return fibonacci(n-2) + fibonacci(n-1)
# print(fibonacci(5))
#
# @clock
# @functools.lru_cache() #备忘功能，避免传入相同参数是重复计算。
# def fibonacci2(n):
#     if n < 2:
#         return n
#     return fibonacci2(n-2) + fibonacci2(n-1)
# print(fibonacci2(6))


#
#######
#
# registry = []
# def register(func):
#     print('running register(%s)' % func)
#     registry.append(func)
#     return func
# @register
# def f1():
#     print('running f1()')
# print('running main()')
# print('registr -> ',registry)
# f1()

#####################

# registry = set()
# def register(active=False):
#     def decorate(func):
#         print('running register(active=%s)->decorate(%s)' % (active,func))
#         if active:
#             registry.add(func)
#         else:
#             registry.discard(func)
#         return func
#     return decorate
#
# @register
# def f1():
#     print('running f1()')
#
# @register
# def f2():
#     print('running f1()')
#
# def f3():
#     print('running f3()')

###################

# import time
# DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'
# def clock(fmt = DEFAULT_FMT):
#     def decorate(func):
#         def clocked(*args):
#             t0 = time.perf_counter()
#             _result = func(*args)
#             elapsed = time.time() - t0
#             name = func.__name__
#             arg_str = ','.join(repr(args) for arg in args)
#             result = repr(_result)
#             print(fmt.format(**locals()))
#             return _result
#         return  clocked
#     return decorate
#
# @clock()
# def snooze(seconds):
#     time.sleep(seconds)
# for i in range(3):
#     snooze(.123)
#
# @clock('{name}:{elapsed}s')
# def snooze(seconds):
#     time.sleep(seconds)
# for i in range(3):
#     snooze(.123)
#
##############
# import copy
# class Bus:
#     def __init__(self,passengers=None):
#         if passengers is None:
#             self.passengers = list()
#         else:
#             self.passengers = list(passengers)
#     def pick(self,name):
#         self.passengers.append(name)
#     def drop(self,name):
#         self.passengers.remove(name)
# bus1 = Bus(['alice','bill','calies','david'])
# bus2 = copy.copy(bus1)
# bus3 = copy.deepcopy(bus2)
# print(id(bus1),id(bus2),id(bus3))
# bus1.drop('bill')
# # bus2.passengers
# print(bus2.passengers)
# print(id(bus1),id(bus2),id(bus3))
# print(id(bus1.passengers),id(bus2),id(bus3))
#########
a = [10,20]
b = [a,30]
a.append(b)
print(a)
from copy import deepcopy
c = deepcopy(a)
print(c)

##########

class HauntedBus:
    def __init__(self,passengers=[]):
        self.passengers = passengers
    def pick(self,name):
        self.passengers.append(name)
    def drop(self,name):
        self.passengers.remove(name)
bus1 = HauntedBus(['alice','bill'])
print(bus1.passengers)
bus1.pick('char')
bus1.drop('alice')
bus2 = HauntedBus()
bus2.pick('carr')   #
print(bus2.passengers)
bus3 = HauntedBus()
print(bus3.passengers)

#################
from array import array
# class Vector2d:
#     typecode = 'd'
#     def __repr__(self):
#         pass
#
#     def __str__(self):
#         pass
#     @classmethod
#     def frombytes(cls):
#         typecode = chr(octets[0])
#         memv = memoryview(octets[1:].cast(typecode))
#         return cls(*memv)
#
################
# class Demo:
#     @classmethod
#     def klassmeth(*args):
#         return args
#
#     @staticmethod
#     def statmeth(*args):
#         return args
# Demo.klassmeth()
# Demo.statmeth('fuck')

##########
s = format(2,'b')
print(s,type(s))
print(format(1/3,'0.4f'))
#######

# class Vector2d:
#     typecode ='d'
#     def __init__(self,x,y):
#         self.__x = float(x)
#         self.__y = float(y)
#     @property
#     def x(self):
#         return self.__x
#     @property
#     def y(self):
#         return self.__y
#     def __iter__(self):
#         return (i for i in (self.x,self.y))
# v1 = Vector2d(3,4)
# print(v1.x,v1.y)

###############
# class Foo:
#     def __getitem__(self, item):
#         return  range(10,20,30)[item]
# f = Foo()
# f[1]

##########
# from random import shuffle
# l = list(range(10))
# print(l)
# shuffle(l)
# print(l)

#########

class A:
    def ping(self):
        print('ping',self)
class B:
    def pong(self):
        print('pong',self)
class C(A):
    def pong(self):
        print('PONG',self)
class D(B,C):
    def ping(self):
        super().ping()
        print('post-ping',self)
    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)
d = D()
d.pong()
C.pong(d)