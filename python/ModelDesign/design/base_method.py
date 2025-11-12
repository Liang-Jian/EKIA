



'''
page 21


方法的介绍
'''
class Person(object):
    def __init__(self,name,age):

        self.name = name
        self.age = age
    def get_person(self):

        return "<Person (%s,%s)>" % (self.name,self.age)

P = Person("john",2)
print("Type Of Object",type(P),"Memory Address",id(P))


a = "john"
b =(1,2,3)
c = [3,4,5,6]
print(a[1],b[0],c[2])
