

'''
page45

工厂方法模式
'''


from abc import ABCMeta,abstractclassmethod


class Section(metaclass=ABCMeta):
    @abstractclassmethod
    def describe(self):
        pass
class PersonalSection(Section):
    def describe(self):
        print("Person Section")
class AlbumSection(Section):
    def describe(self):
        print("Album Section")
class PatentSection(Section):
    def describe(self):
        print("Patent Section")
class PublicaionSection(Section):
    def describe(self):
        print("Publication Section")

class Profile(metaclass=ABCMeta):
    def __init__(self):
        self.section = []
        self.createProfile()
    @abstractclassmethod
    def createProfile(self):
        pass
    def getSection(self):
        return  self.section
    def addSection(self,section):
        self.section.append(section)
class linkedin(Profile):
    def createProfile(self):
        self.addSection(PersonalSection)
        self.addSection(PatentSection)
        self.addSection(PublicaionSection)
class facebook(Profile):
    def createProfile(self):
        self.addSection(PersonalSection)
        self.addSection(AlbumSection)
if __name__ == '__main__':
    profile_type = input("which profile you'd like to create")
    profile = eval(profile_type.lower())()
    print("create profile:...",type(profile).__name__)
    print("Profile has sections --",profile.getSection())



