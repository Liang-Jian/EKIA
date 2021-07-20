from abc import ABCMeta,abstractclassmethod

class Flow(metaclass=ABCMeta):

    @abstractclassmethod
    def run(self): pass