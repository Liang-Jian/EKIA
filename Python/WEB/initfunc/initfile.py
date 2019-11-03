
from abc import ABCMeta,abstractclassmethod

# interface class
class DriVer(metaclass=ABCMeta):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(
                DriVer, cls).__new__(cls, *args, **kwargs)
        return cls.__instance











