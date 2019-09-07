

'''

    page57
    门面模式的应用

'''


class EventManager(object):
    def __init__(self):
        print("Event Manager :: Let me talk to the folks \n")
    def arrange(self):
        self.hotelier = Hotelier()
        self.hotelier.bookHotel()

        self.florist = Florist()
        self.florist.setFlowerRequirements()

        self.caterer = Caterer()
        self.caterer.setCuisine()

        self.musician = Musician()
        self.musician.setMusicType()

class Hotelier(object):
    def __init__(self):
        print("Arranging the hotel for Marriage?--")

    def __isAvailable(self):
        print("Is the hotel free for the event on given day")
        return True
    def bookHotel(self):
        if self.__isAvailable():
            print("Registered the booking \n")
class Florist(object):
    def __init__(self):
        print("Flower Decorations for the Event ?--")
    def setFlowerRequirements(self):
        print("Carnations,roses and lilies would be used for Decorations \n\n")
class Caterer(object):
    def __init__(self):
        print("Food Arrangements for the Event ---")
    def setCuisine(self):
        print("Chinese & Continental Cuisine to be served \n\n")
class Musician(object):
    def __init__(self):
        print("Musical Arrangements for the Marriage --")
    def setMusicType(self):
        print("Jazz and  Classical will be played \n\n")

class You(object):
    def __init__(self):
        print("YOU:: Whoa! Marriage Arrangements??!!")
    def askEventManager(self):
        print("You:: Let's Contact the Event Manager \n\n")
        em = EventManager()
        em.arrange()
    def __del__(self):
        print("YOU:: Thanks to Event Manager,All preparations done! Phew!")

you = You()
you.askEventManager()























