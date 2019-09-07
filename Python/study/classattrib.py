
class People(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        # 私有属性
        self.__number = 0
    # 获取私有属性值  number = p1.number 会执行这个函数

    @property
    def number(self):
        # 返回私有属性值
        return self.__number
    # 设置私有属性值  p1.number = 666
    @number.setter
    def number(self, value):
        # 设置__number的值
        self.__number = value

    # 删除私有属性  del p1.number 会执行这个函数
    @number.deleter
    def number(self):
        del self.__number


class Animal(object):
    def __init__(self,name,weight,hight):
        self.name   = name
        self.weight = weight
        self.hight  = hight

    def eat(self):
        print("eating")
    def sleep(self):
        print("sleeping")

class Dog(Animal):
    def __init__(self,name,weight,hight,legs):
        Animal.__init__(self,name,weight,hight)
        self.legs = legs

    def eat(self):
        print("dog eating")
    def sleep(self):
        print("dog sleep")
if __name__ == '__main__':
    p1 = People('张三', 22)
    # 正常的对象属性赋值
    # 对象.属性名 = 属性值
    p1.name = '李四'
    # 获取对象的属性值
    name = p1.name
    # 删除对象的属性
    del p1.name
    # 私有属性升级版
    # 会去执行@property装饰number函数，函数执行完成后返回一个结果
    num = p1.number
    print(num)
    # 会去执行@number.setter装饰的number函数，在函数中设置__number属性的值
    p1.number = 666
    # 会去执行@property装饰number函数，函数执行完成后返回一个结果
    print(p1.number)
    # 会去执行@number.deleter装饰的number函数，在函数中会将__number属性删除
    del p1.number
    # 会去执行@property装饰number函数，函数执行完成后返回一个结果

