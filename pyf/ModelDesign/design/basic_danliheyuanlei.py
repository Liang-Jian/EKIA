

'''
单例和元类

'''


class Myint(type):
    def __call__(cls, *args, **kwargs):

        print("*****Here'is My int *****",args)
        print("Now do whtever you wwant with these objects...")
        return type.__call__(cls,*args,**kwargs)



class int(metaclass=Myint):
    def __init__(self,x,y):

        self.x = x
        self.y = y


i = int(4,5)