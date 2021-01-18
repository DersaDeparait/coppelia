from code.spider import Spider
from code.neuro import Neuro

class Character:
    iterator = 0
    neuro_father = None
    neuro_mother = None
    characters_all = []

    def __init__(self, person = None, neuro = None):
        if person != None: self.person = person
        else: person = Spider("#{}".format(Character.iterator))

        if neuro != None: self.neuro = neuro
        else: self.neuro = Neuro(mutant_power=1)

        self.fitnes = 0
        self.fitnes_radical = 0

        Character.iterator += 1

        Character.characters_all.append(self)

    def set_neuro(self):
        pass