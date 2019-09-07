


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


print(factorial(3))