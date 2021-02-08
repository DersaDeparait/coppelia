from code.spider import Spider
from code.web import Web
import code.config as code_config
import random
import math

class Character:
    iterator = 0
    web_father = None
    web_mother = None
    characters_all = []
    characters_web_temp = []
    max = 0

    def __init__(self, person = None, web = None):
        if person != None: self.person = person
        else:
            if Character.iterator == 0:
                self.person = Spider()
            else:
                self.person = Spider("#{}".format(Character.iterator-1))

        if web != None: self.web = web
        else: self.web = Web(randomize = 1)

        self.fitnes = 0
        self.fitnes_radical = 0

        Character.iterator += 1

        Character.characters_all.append(self)

    def set_web(self): pass

    def connect_robot(self, client):
        self.person.set_robot(client)

    def iteration_done(self, client):
        self.person.receive_position(client)
        # print(self.person.get_rotation())
        normal_angle = (0, -1.5707963705062866, 0)
        size = -20
        self.fitnes += math.e**(size*(self.person.get_rotation()[1]-normal_angle[1])**2)
        self.fitnes_radical += math.e**(size*(self.person.get_rotation()[1]-normal_angle[1])**2)

        # normal_z = 0.088
        # self.fitnes += math.e**(-200*(self.person.get_position()[2]-normal_z)**2)
        # self.fitnes_radical += math.e**(-200*(self.person.get_position()[2]-normal_z) ** 2)

        # self.fitnes += self.person.get_position()[1] / 10
        # self.fitnes_radical += self.person.get_position()[1] / 10

        print(self.fitnes, self.fitnes_radical)

        self.person.move(client, output_data=self.web.calculate_all(self.person.get_all()))

    def do_end_of_epoch(self):
        # self.fitnes += ((self.person.get_position()[1] + 10) / 20.0) * code_config.CYCLE_TIME
        # self.fitnes_radical += (self.person.get_position()[1]) * 10 * code_config.CYCLE_TIME
        # if self.fitnes_radical <= 0: self.fitnes_radical = 0.001
        # if self.fitnes <= 0: self.fitnes = 0.001
        print(self.fitnes)#, self.fitnes_radical)

    def reset_fitnes(self):
        self.fitnes = 0
        self.fitnes_radical = 0

    @staticmethod
    def calculate_all():
        Character.__calculate_max()
        Character.__make_parents()
        Character.__make_who_not_die()
        Character.__make_new_population()
        Character.__make_mutation()
        Character.__reset_spider_position()

    @staticmethod
    def __calculate_max():
        Character.max = 0
        for i in range(1, len(Character.characters_all)):
            if (Character.characters_all[i].fitnes
                    > Character.characters_all[Character.max].fitnes):
                Character.max = i

    @staticmethod
    def __make_parents():
        Character.__roulette()
    @staticmethod
    def __tournament(): pass
    @staticmethod
    def __roulette():
        index_all = []
        fitnes_all = []
        for i in range(len(Character.characters_all)):
            index_all.append(i)
            fitnes_all.append(Character.characters_all[i].fitnes)

        index_father = random.choices(index_all, fitnes_all, k = 1)[0]
        index_all.pop(index_father)
        fitnes_all.pop(index_father)
        index_mother = random.choices(index_all, fitnes_all, k = 1)[0]

        Character.web_father = Character.characters_all[index_father].web
        Character.web_mother = Character.characters_all[index_mother].web

    @staticmethod
    def __make_who_not_die():
        index_all = []
        fitnes_all = []
        for i in range(len(Character.characters_all)):
            index_all.append(i)
            fitnes_all.append(Character.characters_all[i].fitnes)

        Character.characters_web_temp = []
        for i in range(code_config.COUNT_OF_ALIVE_AFTER_EPOCH):
            index = random.choices(index_all, fitnes_all, k = 1)[0]
            Character.characters_web_temp.append(Character.characters_all[index].web)
            index_all.remove(index)
            fitnes_all.remove(Character.characters_all[index].fitnes)

    @staticmethod
    def __make_new_population():
        start = len(Character.characters_web_temp)
        for i in range(start, code_config.NUMBER_OF_SPIDERS):
                Character.characters_web_temp.append(Character.web_father.cross_crossover_one(Character.web_mother))

        for i in range(len(Character.characters_all)):
            Character.characters_all[i].web = Character.characters_web_temp[i]

    @staticmethod
    def __make_mutation():
        for i in range(len(Character.characters_all)):
            Character.characters_all[i].web.make_mutation(code_config.MUTATION_POWER)

    @staticmethod
    def __reset_spider_position():
        for i in range(len(Character.characters_all)):
            Character.characters_all[i].person.reset_position()



    @staticmethod
    def save_to_db_fitnes():
        d = {}
        for i in range(len(Character.characters_all)):
            d["f_{}".format(i)] = [Character.characters_all[i].fitnes]
            d["fr_{}".format(i)] = [Character.characters_all[i].fitnes_radical]
        return d

    @staticmethod
    def save_to_db_last_web():
        d = {}
        d.update(Character.characters_all[Character.max].web.axon_line(0))
        return d