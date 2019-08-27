

# page49

import copy
from collections import OrderedDict


class Book:

    def __init__(self,name,authors,price,**rest):
        self.name = name
        self.authors = authors
        self.price =price
        self.__dict__.update(rest)


    def __str__(self):
        mylist = []
        orderd = OrderedDict(sorted(self.__dict__.items()))
        for i in orderd.keys():
            mylist.append('{}:{}'.format(i,orderd[i]))
            if i == 'price':
                mylist.append('$')
            mylist.append('\n')
        return ''.join(mylist)

class Prototype:
    def __init__(self):
        self.objects = dict()
    def register(self,identifier,obj):
        self.objects[identifier] = obj
    def unregister(self,identifier):
        del self.objects[identifier]
    def clone(self,identifier,**attr):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError('Incorrect object identifier:{}'.format(identifier))
        obj = copy.deepcopy(found)
        obj.__dict__.update(attr)
        return obj

def main():
    b1 =  Book('The C Programing Langueage',('Brain W.Kernighan','Dennis M.Ritchie'),
    price =118,publisher='Prentice Hall',length=228,publication_date = '1978-2-28',
    tags=('C','programing','algorhams','data-structures'))


    prototype = Prototype()
    cid = 'k&r-first'
    prototype.register(cid,b1)
    b2 = prototype.clone(cid,name='The C Programming Language(ANSI)',price=48.99,length=274,pblication_date='1988-04-01'
    ,edition=2)

    for i in (b1,b2):
        print(i)
    print("ID b1 :{} != ID b2 :{}".format(id(b1),id(b2)))

if __name__ == '__main__':
    main()


