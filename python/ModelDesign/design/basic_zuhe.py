

'''

组合
'''


class A(object):
    def a1(self):
        print("a1")
class B(object):
    def b1(self):
        print("b")
        A().a1()

b = B()
b .b1()