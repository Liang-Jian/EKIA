

'''
page 22
继承的介绍

'''


class A:
    def a1(self):
        print("a1")


class B(A):
    def b1(self):
        print("b1")

b = B()
b.a1()