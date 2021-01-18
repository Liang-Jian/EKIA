from abc import ABCMeta,abstractclassmethod

class ApiTestSchedulerNew:
    pass


class FlowTestCase:
    pass



class ICaseEntityFlow(metaclass=ABCMeta):
    @abstractclassmethod
    def run(self):
        pass

