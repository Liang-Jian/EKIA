import os


'''
python adventr from youtube
'''

from string import Template
import argparse
# class MyTemplate(Template):
#     delimiter = "#"
# def Main():
#     cart = []
#     cart.append(dict(item='Coke',price=8,qty=2))
#     cart.append(dict(item='Coke',price=12,qty=1))
#     cart.append(dict(item='Fish',price=32,qty=4))
#     # t = Template("$qty x $item = $price")
#     t = MyTemplate("#qty x #item = #price")
#     total =0
#     print("Cart: ")
#     for data in cart:
#         print(t.substitute((data)))
#         total +=data["price"]
#     print("total: = " + str(total))
# if __name__ == '__main__':Main()

##------> < ------##
# def fib(n):
#     a,b = 0,1
#     for i in range(n):
#         a,b = b,a+b
#     return  a
#
# def Main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("num",help="The Fbinonacci numver you wish to calculate",type=int)
#     parser.add_argument("-v","--verbose",action="store_true")
#     args = parser.parse_args()
#     result = fib(args.num)
#     if args.verbose:
#         print("The " + str(args.num) + th)
#     elif args.quiet:
#         print(result)
#     else:
#         print("Fib("+ str(args.num) + str(result))
#     # print("The " + str(args.num) + "th fib number is  "+str(result))
# if __name__ == '__main__': Main()

#
# import os,re,argparse
# def main():
#     line = " I think undrestan regular expressions"
#     matchRelt = re.match('think',line,re.M|re.I)
#     if matchRelt:
#         print("MatchFound: " + matchRelt.group(()))
#     else:
#         print("No Match was Found")
#     searchResult = re.search('think', line,re.M|re.I)
#     if searchResult:
#         print("Search Found: " + searchResult.group())
#     else:
#         print("Nothing found in search")
# if __name__ == '__main__': main()
#
##--------------><---------------#


# def main():
#     parser =  argparse.ArgumentParser()
#     parser.add_argument()
#     parser.add_argument()

##--------------><----------------#
# import re
# def Main():
#     line = "I think I understatnd regular expression"
#     matchResult = re.match('think',line,re.M|re.I)
#     if matchResult:
#         print("Match Found: "+ matchResult.group())
#     else:
#         print("No match was Found")
#     searchResult = re.search("think",line,re.M|re.I)
#     if searchResult:
#         print("Search Found " + searchResult.group())
#     else:
#         print("No Search was Found")
# Main()
#-------------<>--------------#

# from threading import  Thread
# import time
# def timer(name,delay,repeat):
#     print("Timer: " + name + "Started")
#     while repeat >0:
#              time.sleep(delay)
#              print(name + "1 "+ str(time.ctime(time.time())))
#              repeat -=1
#     print("Timer: " + name + "Completed")
# def Main():
#     t1 = Thread(target=timer,args=("Timer1",1,5))
#     t2 = Thread(target=timer,args=("Timer2",2,5))
#     t1.start()
#     t2.start()
#     print("Main Completed")
# if __name__ == '__main__':
#     Main()
#---------<>----------#
# import threading,time
# class AsynWrite(threading.Thread):
#     def __init__(self,text,out):
#         threading.Thread.__init__(self)
#         self.text = text
#         self.out = out
#
#     def run(self):
#         f = open(self.out,"a")
#         f.write(self.text + '\n')
#         f.close()
#         time.sleep(2)
#         print("Finedsh Baclgout File write to "+ self.out)
# def Main():
#     message = input("Enter a string to store")
#     background = AsynWrite(message,'out.txt')
#     background.start()
#     print("the program can continue while it writes in another threader")
#     print("100 + 400=",100+100)
#     background.join()
#     print("Waited until thread was complete")
# if __name__ == '__main__':
#     Main()
#----------<>----------#
# import time,threading
# tLock = threading.Lock()
# def timer(name,delay,repeat):
#     print("Timer: " + name + "Started")
#     tLock.acquire()
#     while repeat >0:
#              time.sleep(delay)
#              print(name + "1 "+ str(time.ctime(time.time())))
#              repeat -=1
#     print(name + " is release the lock")
#     tLock.release()
#     print("Timer: " + name + "Completed")
# def Main():
#     t1 = threading.Thread(target=timer,args=("Timer1",1,5))
#     t2 = threading.Thread(target=timer,args=("Timer2",2,5))
#     t1.start()
#     t2.start()
#     print("Main Completed")
# if __name__ == '__main__':
#     Main()
#----------<>------------#

# import socket
# def Main():
#     host = "127.0.0.1"
#     port =5000
#     s = socket.socket()
#     s.bind()


#------------------------=

# import matplotlib.axes as plt
# import numpy as np
#
# my_x = np.linspace(-1,1)
# my_y = np.sin(my_x)
#
# plt.plot(my_x,my_y)
# title = "Plot"
# filename = "plot.jpg"
# plt.title(title)
# plt.savefig(filename)

###############

# class DOg:
#     def __init__(self):
#         self.bank()
#     def a(self):
#         pass


# def make_class(x):
#     class Dog:
#         def __init__(self,name):
#             self.name = name
#         def print_value(self):
#             print(x)
#     return Dog
# cls = make_class(10)
# print(cls)
#
# d = cls("fuck")
# print(d.name)
# d.print_value()


#######################

# for i in range(10):
#     def show():
#         print(i*2)
#     # show()  # xiao guo bu tong
# show()

############
import inspect
def func(x):
    if x== 1:
        def rv():
            print("X is equesl to 1 ")
    else:
        def rv():
            print("X is not 1")
    return rv()
new_func  = func(2)
print(new_func(inspect.getmembers(new_func)))
new_func(inspect.getmembers(new_func))