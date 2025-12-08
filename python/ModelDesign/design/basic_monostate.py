

'''
monostate 模式可以通过


'''
'''
class Borg:
    __share_state = {"1":"2"}
    def __init__(self):

        self.x = 1
        self.__dict__= self.__share_state


b = Borg()
b1 = Borg()
b.x=4

print("Borg Object 'b':",b)
print("Borg Object 'b1':",b1)
print("Borg Object 'b':",b.__dict__)
print("Borg Object 'b1':",b1.__dict__)
'''


class Borg:
    __share_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Borg, cls).__new__(cls,*args,**kwargs)
        obj.__dict__ = cls.__share_state
        return obj

















