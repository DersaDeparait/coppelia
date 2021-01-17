from code.spider import Spider
from code.neuro import Neuro

class Character:
    iterator = 0
    def __init__(self, person = None, neuro = None):
        if person != None: self.person = person
        else: person = Spider("#{}".format(Character.iterator))

        if neuro != None: self.neuro = neuro
        else: self.neuro = Neuro()

        self.fitnes = 0

        Character.iterator += 1


