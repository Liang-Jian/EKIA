


from abc import ABCMeta,abstractclassmethod,abstractmethod

def fibonaci():
    a,b = 0,1
    while True:
        yield a
        a,b = b, a+b
        # print(a,b)


class CreditCard:
    """ A consumer creadit card """
    def __init__(self,customter,bank,account,limit):
        """Create new creadi card instance

        :param customter:
        :param bank:
        :param account:
        """
        self._customter = customter
        self._bank  = bank
        self._account = account
        self._balance = 0
        self._limit = limit

    def get_customer(self):
        """ Return name of the customer"""
        return self._customter

    def get_bank(self):
        """ Retutn bank of name"""
        return self._bank

    def get_account(self):
        """Return the card identify number"""
        return self._account

    def get_limit(self):
        """Return current creadit limit"""
        return  self._limit

    def get_balance(self):
        """Return current balance"""
        return  self._balance

    def charge(self,price):
        """Charge give price to the card ,assuringsufficient creandit limit"""

        if price + self._balance > self._limit:
            return False
        else:
            self._balance += price
            return True
    def make_payment(self,amount):
        """Proce customer paymet that reduces balance"""
        self._balance -=amount

cc = CreditCard("john","1st bank",'23439039 9239 8432',1999)

class Vector:
    """Represend a ventor in a multidimensional space """

    def __init__(self,d):
        """Create d-dimesion al vector of zeros"""
        self._coords = [0] * d

    def __len__(self):
        """Return  the dimension of the vector"""
        return  len(self._coords)

    def __getitem__(self, item):
        return self._coords[item]

    def __setitem__(self, key, value):
        self._coords[key] = value

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError("dimesions must agree")
        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result

    def __eq__(self, other):
        return self._coords == other._coords

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '<' + str(self._coords)[1:-1] + '>'


class SequenceIterator:
    def __init__(self,sequence):
        self._seq = sequence
        self._k  = -1
    def __next__(self):
        self._k +=1
        if self._k < len(self._seq):
            return (self._seq[self._k])
        else:
            raise StopIteration
    def __iter__(self):
        return self


class Range:
    def __init__(self,start,stop=None,step=1):
        if step == 0:
            raise ValueError('step connt be O')
        if stop is None:
            start,stop = 0 ,start
        self._length = max(0,stop-start+step-1 // step)
        self._start = start
        self._step = step

    def __len__(self):
        return self._length

    def __getitem__(self, item):
        if item <0:
            item+=len(self)
        if not  0 < item < self._length:
            raise IndexError('index out of range')
        return self._start + k * self._step



class PredatoryCreditCard(CreditCard):
    def __init__(self,customter,bank,account,limit,apr):
        super().__init__(customter,bank,account,limit,apr)
        self._apr = apr

    def charge(self,price):
        """Charge give price to the card,assuring sufficient credit limit"""
        success = super().charge(price)
        if not success:
            self.get_balance +=5
        return success

    def process_month(self):
        if self._balance > 0:
            monthly_factor = pow(1+self._apr ,1 /12 )
            self._balance *=monthly_factor


class Progression:
    def __init__(self,start = 0):
        self._current = start
    def _advance(self):
        self._current +=1
    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            answer = self._current
            self._advance()
            return answer
    def __iter__(self):
        return self

    def print_progression(self,n):
        print(" ".join(str(next(self) for j in range(n))))

class ArithmeticPrograssion(Progression):
    def __init__(self,increment=1,start=0):
        """
        等差数列
        :param increment:
        :param start:
        """
        super().__init__(start)
        self._increment = increment
    def _advance(self):
        self._current += self._increment

class GeometricProgression(Progression):
    def __init__(self,base = 2, start =1):
        """
        等比数列
        :param base:
        :param start:
        """
        super().__init__(start)
        self._base = base
    def _advance(self):
        self._current *= self._base


class FibonacciProgression(Progression):
    def __init__(self,first=0,second=1):
        super().__init__(first)
        self._prev = second - first

    def _advance(self):
        self._prev,self._current = self._current,self._prev + self._current


class Sequence(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self):
        """"""
    def __getitem__(self, item):
        """"""
    def __contains__(self, val):
        """"""
        for j in range(len(self)):
            if self[j] == val:
                return True
            else:
                return False




from copy import deepcopy
a = ['a','b','c']
b = deepcopy(a)
b.append('d')
print(a)
print(b)

# if __name__ == '__main__':
#     print(FibonacciProgression(4,5).print_progression(10))


from time import time
start_time = time()

# run algori
end_time = time()

chayi = end_time - start_time


def gaosi():
    st =time()
    a = 0
    for i in range(1,101):
        a+=i
    dt = time()
    print(a)
    print(dt-st)



def find_max(data):
    biggest = data[0]
    for val in data:
        if val > biggest:
            biggest = val
    return biggest
print(find_max([2,3,4,5]))



def prefix_ave(s):#  求和
    n = len(s)
    A =[0] * n
    for j in range(n):
        total = 0
        for i in range(j+1):
            total +=s[i]
        A[j] = total / (j+1)
    return A


def prefix_ave2(s):
    n = len(s)
    A = [0] * n
    for j in range(n):
        A[j] = sum(s[0:j+1]) / (j+1)
    return A

def prefix_ave3(s):
    n  = len(s)
    A = [0] * n
    total = 0
    for j in range(n):
        total += s[j]
        A[j] = total / (j+1)
    return A

# print(prefix_ave3(100))



def disjoin1(A,B,C):
    for a in A:
        for b in B:
            for c in C:
                if a == b == c:
                    return False
    return True


def disjoin2(A,B,C):
    for a in A:
        for b in B:
            if a==b:
                for c in C:
                    if a ==c :
                        return False
    return True

def unique1(S):
    for j in range(len(S)):
        for k in range(j+1,len(S)):
            if S[j] == S[k]:
                return False
    return True

def unique2(S):
    temp = sorted(S)
    for j in range(1,len(temp)):
        if temp[j-1] == temp[j]:
            return False
    return True

print(disjoin2(['a','b'],['c','d'],['e','f']))


def factorial(n):
    if n==0:
        return n
    else:
        return n * factorial(n-1)


################
#
#   基于数据的序列
#
################
import ctypes

class DynamicArray:
    def __init__(self):
        self._n = 0
        self._capacity =1
        self._A = self._make_array(self._capacity)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        if not 0 <= k  < self._n:
            raise IndexError('invalid index')
        return self._A[k]

    def append(self,obj):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n +=1

    def _resize(self,c):
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def insert(self,k,value):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._n,k,-1):
            self._A[j] = self._A[j-1]
        self._A[j] = value
        self._n += 1

    def remove(self,value):
        for k in  range(self._n):
            if self._A[k] == value:
                for j in range(k,self._n -1):
                    self._A[j] = self._A[j+1]
                self._A[self._n -1] = None
                self._n -=1
                return
            raise ValueError('value not found')
    def _make_array(self,c):
        return (c * ctypes.py_object)()


from time import time

def compute_average(n):
    data = []
    start = time()
    for k in range(n):
        data.append(None)
    end = time()
    return (end-start) / n



class GameEntry:

    def __init__(self,name,score):
        self._name = name
        self._score = score

    def get_name(self):
        return self._name

    def get_score(self):
        return self._name

    def __str__(self):
        return '({0},{1})'.format(self._name,self._score)


class Scoreboar:

    def __init__(self,capacity=10):
        self._board = [None] * capacity
        self._n = 0

    def __getitem__(self, item):
        return self._board[item]

    def __str__(self):
        return '\n'.join(str(self._board[j]) for j in range(self._n))

    def add(self,entry):
        score = entry.get_score()
        good = self._n < len(self._board) or score > self._board[-1].get_score()

        if good:
            if self._n < len(self._board):
                self._n +=1
            j = self._n -1
            while j> 0 and self._board[j-1].get_score() < score:
                self._board[j] = self._board[j-1]
                j -= 1
            self._board[j] = entry


def insertion_sort(A):
    for k in range(1,len(A)):
        cur  = A[k]
        j = k
        while j > 0 and  A[j-1] > cur:
            A[j] = A[j-1]
            j -=1
        A[j] = cur


class CaesarCipher:
    def __init__(self,shift):
        encoder = [None] * 26
        decoder = [None] * 26

        for k in range(26):
            encoder[k] = chr(k + shift) % 26 + ord('A')
            decoder[k] = chr(k - shift) % 26 + ord('A')
        self._forward = ''.join(encoder)
        self._backwrd = ''.join(decoder)

    def encrypt(self,message):
        return self._transform(message,self._forward)

    def decrypt(self,secret):
        return self._transform(secret,self._backwrd)

    def _tranform(self,original,code):
        msg = list(original)
        for k in range(len(msg)):
            if msg[k].isupper():
                j = ord(msg[k]) - ord('A')
                msg[k] = code[j]
            return ''.join(msg)

# if __name__ == '__main__':
#     cipher = CaesarCipher(3)
#     message = 'The EAGE'



############################


# stack queue

class ArrayStack:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self,e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty('stack is empth')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty('stack is empty')
        return self._data.pop()


def reverse_file(filename):
    S = ArrayStack()
    original = open(filename)
    for line in original:
        S.push(line.rsplit('\n'))
    original.close()

    output = open(filename,'w')
    while not S.is_empty():
        output.write(S.pop() + '\n')
    output.close()
# if __name__ == '__main__':
#     cipher = CaesarCipher(3)
#     message = "The eaglesis in play; meet as jobs"
#     coded = cipher.encrypt(message)
#     print('Secret ',coded)
#     answer = cipher.decrypt(coded)
#     print("Message ",answer)


def is_matched_html(raw):
    S = ArrayStack()
    j = raw.find("<")
    while j != -1:
        k = raw.find(">",j + 1)
        if k== -1:
            return False
        tag = raw[j+1:k]
        if not tag.startwith('/'):
            S.push(tag)
        else:
            if S.is_empty():
                return False
            if tag[1:] != S.pop():
                return False
        j = raw.find("<",k+1)
    return S.is_empty()


