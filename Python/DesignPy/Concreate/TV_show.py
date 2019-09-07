

from abc import abstractclassmethod,ABCMeta

class State(metaclass=ABCMeta):

    @abstractclassmethod
    def doThis(cls):
        pass

class StartState(State):
    def doThis(cls):
        print("TV shitching on..")

class StopState(State):
    def doThis(cls):
        print("TV switching off.")


class TVContext(State):

    def __init__(self):
        self.state =None

    def getState(self):
        return self.state

    def setState(self,state):
        self.state = state

    def doThis(self):
        self.state.doThis()

context = TVContext()
context.getState()

start = StartState()
stop = StopState()

context.setState(stop)
context.doThis()
