

'''
工厂模式,
page42

定义一个接口animal,创建子类的功能交给子类
'''

from abc import ABCMeta,abstractclassmethod

class Animal(metaclass=ABCMeta):
    @abstractclassmethod
    def do_say(self):
        pass

class Dog(Animal):
    def do_say(self):
        print("wangwang")

class Cat(Animal):
    def do_say(self):
        print("miaomiao")

class ForestFactory(object):
    def make_souond(self,object_type):
        return eval(object_type)().do_say()

if __name__ == '__main__':
    ff = ForestFactory()
    animal = input("Which animal should make_sound Dog or Cat?")
    ff.make_souond(animal)