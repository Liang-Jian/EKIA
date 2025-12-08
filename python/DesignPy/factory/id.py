


class A(object):
    pass


a = A()
b = A()


print(id(a) == id(b))
print(a,b)