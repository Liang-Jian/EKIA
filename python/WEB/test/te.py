


from abc import ABCMeta,abstractclassmethod
from selenium import webdriver




class Compiler(metaclass=ABCMeta):
    @abstractclassmethod
    def collectSource(self):
        pass
    @abstractclassmethod
    def compileToObject(self):
        pass
    @abstractclassmethod
    def run(self):
        pass
    def compileAndRun(self):
        self.collectSource()
        self.compileToObject()
        return self.run()


class iOSCompiler(Compiler):
    def collectSource(self):
        print("Collecting swift Source Code")
    def compileToObject(self):
        print("Compiling Swift code to LLVM bitcode")
    def run(self):
        print("Program runing on runtime environment")

        str = "sf"+"dfs"

        return str


# iOS = iOSCompiler()
#
# iOS.compileAndRun()
#
# print(iOS.compileAndRun())