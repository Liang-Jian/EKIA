

from interface.interfaceflow import Flow
from flow.lexue import LeXue


class AllFlow(Flow):
    def run(self):
        LeXue().run()

if __name__ == '__main__':
    AllFlow().run()
