

import  re
'''
m = re.match('foo','foo')
if m is not None:
    print(m.group())


n = re.match('foo','food on the table')
print(n.group())

print (re.match('foo','foo is in ').group())

m = re.match('foo','seafood')
if m is not None:m.group()

bt = 'com|net|org'
m = re.match(bt,'net')
if m is not None:print(m.group())


n = re.search(bt,'ww.google.com')
if n is not None: print(n.group())
'''

anyend = '.end'
m =re.match(anyend,'bend')
if m is not None:print(m.group())

# m = re.match(anyend,'end')
m = re.match(anyend,'\nend')
if m is not None:print(m.group())


m = '3.14'
pi_patt = '3\.14'
s =re.search(m,'3.14')
if s is not None:print(s.group())
k = re.search(pi_patt,'3.14')
if k is not None:print(k.group())

m = re.match(m,'3014')
if m is not None:print(m.group())

# m = re.match('[cr][23][dp][o2]]','c3po')
m = re.match('[cr][23][dp][o2]','c2po')
if m is not None:print(m.group())

m = re.match('[cr][23][dp][o2]','c2do')
if m is not None:print(m.group())

m = re.match('r2d2|c3po','c2do')
if m is not None:print(m.group())

patt = '\w+@(\w+\.)?\w+\.com'
print(re.match(patt,'obody@xxx.comm').group())

# patt = '\w+@(\w+ \.)*\w+\.com'
# print (re.match(patt,'nobody@www.xxx.yyy.zzz.com').group())

m = re.match('\w\w\w-\d\d\d','abc-123')
if m is not None:print(m.group())

m = re.match('(\w\w\w)-(\d\d\d)','abc-123')
if m is not None:print (m.group(2))

m = re.match('(a(b))','ab')
if m is not None:print(m.group(2),m.groups())

m = re.search('^the','the end.')
if m is not None:print (m.group())

m = re.search('^the','end the')
if m is not None:print(m.group())

m = re.search(r'\bthe','bite the dog')
if m is not None:print (m.group())

m = re.search(r'\bthe','bitethe dog')
if m is not None:print(m.group())

m = re.search(r'\Bthe','bitethe dog')
if m is not None:print(m.group())

m = re.findall('car','car')
if m is not None:print(m)

m = re.findall('car','scary')
if m is not None:print(m)

m = re.findall('car','scar is cary\' s cars')
if m is not None:print(m)

m = re.sub('[ae]','X','abcdef')

if m is not None:print(m)

m = re.subn('[ae]','X','abcdef')
if m is not None:print(m)

m = re.split(':','abc:edf:efo')
if m is not None:print(m)
'''
from random import randint,choice
from string import ascii_lowercase
from sys import maxsize
from time import ctime

doms = {'com','edu','net','gov','org'}
for i in range(randint(5,10)):
    dtint = randint(0,maxsize-1)
    dtstr = ctime(dtint)
    shorter = randint(4,7)
    em = ''
    for j in range(shorter):
        em += choice(ascii_lowercase)
    longer = randint(shorter,12)
    dn = ''
    for j in range(longer):
        dn += choice(ascii_lowercase)
    print ('%s :: %s@%s.%s::%d-%d-%d' % (dtstr,em,dn,choice(doms),dtint,shorter,longer))
'''
data = 'Thu Feb 15 17:46:03 2007::uzifzf@dpyivihw.gov::1171590364-6-8'
patt = ('^mon|Tue|Wed|Thu|Fri|Sat|Sun')
m = re.match(patt,data)
if m is not None:print(m.group())

patt = ('^(\w){3}')
m = re.match(patt,data)
if m is not None:print(m.groups())

patt = '\d+-\d+-\d+'
m = re.search(patt,data).group()
if m is not None:print(m)

patt = '.+\d+-\d+-\d+'
m = re.search(patt,data).group()
if m is not None:print(m)

patt = '.+(\d+-\d+-\d+)'
m = re.search(patt,data).group(1)
if m is not None:print(m)

patt = '.+?(\d+-\d+-\d+)'#非贪婪模式
m = re.search(patt,data).group(1)
if m is not None:print(m)

patt = '-(\d+)-'
m = re.search(patt,data).group()
m1 = re.search(patt,data).group(1)
if m is not None:print(m)
if m1 is not None:print(m1)




'''
from time import sleep,ctime
import _thread
def loop0():
    print('start loop 0 at :',ctime())
    sleep(4)
    print ('loop 0 done at :',ctime())
def loop1():
    print('start loop 1 at:',ctime())
    sleep(2)
    print ('loop1 done at :',ctime())
def main():
    print ('starting at:',ctime())
    _thread.start_new_thread(loop0,())
    _thread.start_new_thread(loop1,())
    sleep(3)
    print ('all Done at:',ctime())
if __name__ == '__main__':
    main()
'''
'''
import  threading
from time import sleep,ctime
loops= [4,2]

def loop(nloop,nsec):
    print('start loop',nloop,'at:',ctime())
    sleep(nsec)
    print('loop',nloop,'done at:',ctime())
def main():
    print('starting at:',ctime())
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop,args=(i,loops[i]))
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
    print('all Done at:',ctime())
if __name__ == '__main__':
    main()


import threading
from time import sleep,ctime

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    def getResult(self):
        return self.res
    def run(self):
        print('starting',self.name,'at:',ctime())
        self.res = self.func,self.args
        print(self.name,'finished at:',ctime())


'''

from random import randint
from time import sleep
import queue
def writeQ(queue):
    print('producing object for Q...')
    queue.put('xxx',1)
    print('size now ',queue.qsize())
def readQ(queue):
    val = queue.get(1)
    print('consumed object from Q .. size now',queue.qsize())
def write(queue,loops):
    for i in range(loops):
        writeQ()
        sleep(randint(1,3))
def reader(queue,loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer,reader]
nfuncs = range(len(funcs))

def main():
    nlops= randint(2,5)
    q = Queue(323)
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i],(q,nlops),funcs[i].__name__)
        threads.append(t)
    for i in nfuncs:
        threads.start()
    for i in nfuncs:
        threads.join()
    print('all Done')


if __name__ == '__main__':
    main()