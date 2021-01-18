from random import choices
import random
import time
from datetime import datetime

import b0RemoteApi

from code.spider import Spider
from code.neuro import Neuro
from code.excel import ExcelManager
import code.config as code_config

class Scene:
    def __init__(self):
        self.__init_log()
        self.__init_coppelia()
        self.__init_loop_params()
        self.__init_config()
        self.__init_create_spiders()
        self.__init_read_from_file()
    def __init_coppelia(self):
        self.python_client = 'b0RemoteApi_pythonClient'
        self.remote_api = 'b0RemoteApi_first'
        self.client = None
    def __init_loop_params(self):
        self.do_next_step = True
        self.flag = True
        self.counter = 0
        self.epoch = 0
    def __init_config(self):
        self.number_of_spiders = code_config.NUMBER_OF_SPIDERS
        self.life_time = code_config.CYCLE_TIME
        self.count_of_alive_after_epoch = code_config.COUNT_OF_ALIVE_AFTER_EPOCH
        self.mutation_power = code_config.MUTATION_POWER
    def __init_create_spiders(self):
        self.spiders = [Spider(), Spider("#0"), Spider("#1"), Spider("#2")
            , Spider("#3"), Spider("#4"), Spider("#5"), Spider("#6")
            , Spider("#7"), Spider("#8"), Spider("#9"), Spider("#10")
            , Spider("#11"), Spider("#12"), Spider("#13"), Spider("#14")
            , Spider("#15"), Spider("#16"), Spider("#17"), Spider("#18")
            , Spider("#19"), Spider("#20"), Spider("#21")  # , Spider("#22")
                        ]

        self.neuro = []
        self.neuro_father = Neuro()
        self.neuro_mother = Neuro()
        self.neuro.append(Neuro())
        self.fitnes = [0] * len(self.spiders)
        self.fitnes_radical = [0] * len(self.spiders)
    def __init_read_from_file(self):
        self.excel = ExcelManager(name=2, size=len(self.spiders))
        high, weigh = self.excel.read(0)
        if (high != None):

            count = 0
            for i in range(len(self.neuro[0].axon_weigh)):
                to_add = count
                for j in range(len(self.neuro[0].axon_weigh[i])):
                    for k in range(len(self.neuro[0].axon_weigh[i][j])):
                        count += 1
                        self.neuro[0].axon_weigh[i][j][k] \
                            = weigh[to_add + k + j * len(self.neuro[0].axon_weigh[i][j])]

            for w in range(1, len(self.spiders)):
                high, weigh = self.excel.read(w)
                self.neuro.append(Neuro())
                count = 0
                for i in range(len(self.neuro[w].axon_weigh)):
                    to_add = count
                    for j in range(len(self.neuro[w].axon_weigh[i])):
                        for k in range(len(self.neuro[w].axon_weigh[i][j])):
                            count += 1
                            self.neuro[w].axon_weigh[i][j][k] \
                                = weigh[to_add + k + j * len(self.neuro[w].axon_weigh[i][j])]
        else:
            for i in range(1, len(self.spiders)):
                self.neuro.append(Neuro(mutant_power=1))
    def __init_log(self):
        self.show_info = code_config.SHOW_INFO # Виводить в консоль дані
        self.time_start = datetime.now()
        self.time_last_print = datetime.now()
        self.time_after_beggining = 0
        self.time_after_last_print = 0

    def __print_time(self, message = ""):
        if self.show_info:
            self.time_after_beggining = datetime.now() - self.time_start
            self.time_after_last_print = datetime.now() - self.time_last_print
            self.time_last_print = datetime.now()
            print("{0}  -  {1}".format(self.time_after_last_print, self.time_after_beggining))
            print(message)



    def start(self):
        while True:
            with b0RemoteApi.RemoteApiClient(self.python_client, self.remote_api) as self.client:
                self.add_method()
                self.add_objects()
                self.start_simulation()
                self.loop()
                self.finish_simulation()
                self.remake_neural_network()
            time.sleep(1)
    def add_method(self):
        self.client.simxSynchronous(True)
        self.client.simxGetSimulationStepStarted(self.client.simxDefaultSubscriber(self.simulationStepStarted))
        self.client.simxGetSimulationStepDone(self.client.simxDefaultSubscriber(self.simulationStepDone))
    def add_objects(self):
        #err_hand_cube, self.obj_hund_cube = self.client.simxGetObjectHandle('Cuboid', self.client.simxServiceCall())
        for spider in self.spiders:
            spider.set_robot(self.client)
    def start_simulation(self):
        self.client.simxStartSimulation(self.client.simxDefaultPublisher())
    def loop(self):
        while self.flag:
            if self.do_next_step:
                self.do_next_step = False
                self.client.simxSynchronousTrigger()
            self.client.simxSpinOnce()
    def finish_simulation(self):
        self.client.simxStopSimulation(self.client.simxDefaultPublisher())
    def remake_neural_network(self):
        self.counter = 0
        self.flag = True


        # self.fitnes = []
        # self.fitnes_radical = []
        for i in range(len(self.spiders)):
            self.fitnes[i] += ((self.spiders[i].get_position()[1] + 10) / 20.0) * self.life_time
            self.fitnes_radical[i] += (self.spiders[i].get_position()[1]) * 10 * self.life_time
            if self.fitnes_radical[i] <= 0: self.fitnes_radical[i] = 0.001
            if self.fitnes[i] <= 0: self.fitnes[i] = 0.001
            print(self.fitnes[i], self.fitnes_radical[i])


        max = 0
        for i in range(1, len(self.spiders)):
            if (self.fitnes[i]> self.fitnes[max]):
                max = i
                print(max, self.spiders[max].get_position()[1])
        self.excel.write_data2D_best(self.fitnes[max], self.neuro[max].axon_weigh)
        # print("best: ", max, "//", len(self.neuro))
        # for i in range(len(neuro_best.axon_weigh)):
        #     for j in range(len(neuro_best.axon_weigh[i])):
        #         print(i, j, neuro_best.axon_weigh[i][j])


        self.__make_parents()
        self.__make_who_not_die()
        self.__make_new_population()
        self.__make_mutation()
        self.__save_to_db()


    def __make_parents(self):
        self.__roulette()
    def __tournament(self): pass
    def __roulette(self):
        index = []
        for i in range(len(self.neuro)):
            index.append(i)
        print(index)
        self.index_father = choices(index, weights = self.fitnes_radical, k = 1)[0]
        self.index_mother = choices(index, weights = self.fitnes_radical, k = 1)[0]
        while self.index_father == self.index_mother:
            self.index_mother = choices(index, weights=self.fitnes_radical, k=1)[0]
        self.neuro_father = self.neuro[self.index_father]
        self.neuro_mother = self.neuro[self.index_mother]
        self.excel.write_data2D_father(self.fitnes[self.index_father], self.neuro_father.axon_weigh)
        self.excel.write_data2D_mother(self.fitnes[self.index_mother], self.neuro_mother.axon_weigh)

    def __make_who_not_die(self):
        self.alive = []
        index = []
        for i in range(len(self.neuro)):
            index.append(i)
        print(index)
        self.alive.append(choices(index, weights = self.fitnes_radical, k = 1)[0])
        for i in range(self.count_of_alive_after_epoch - 1):
            else_number = choices(index, weights = self.fitnes_radical, k = 1)[0]
            while else_number in self.alive:
                print("Same {}".format(else_number))
                else_number = choices(index, weights=self.fitnes_radical, k=1)[0]
                print("new {}, all {}".format(else_number, self.alive))
            self.alive.append(else_number)





    def __make_new_population(self):
        neuro_new = []
        for i in range(self.count_of_alive_after_epoch):
            neuro_new.append(self.neuro[self.alive[i]])
        self.neuro = neuro_new
        for i in range(self.count_of_alive_after_epoch, len(self.spiders)):
            if random.random() > 0.5:
                self.neuro.append(Neuro.crossover_one(self.neuro_father, self.neuro_mother))
            else:
                self.neuro.append(Neuro.crossover_one(self.neuro_mother, self.neuro_father))
        for i in range(len(self.spiders)):
            self.spiders[i].reset_position()

    def __make_mutation(self):
        for i in range(len(self.spiders)):
            self.neuro[i].make_mutation(self.mutation_power)
        print("Зроблена мутація")

    def __save_to_db(self):
        print("Почався запис в ексель")
        for i in range(len(self.spiders)):
            self.excel.write_data2D(i, self.fitnes[i], self.neuro[i].axon_weigh)
        print("Завершився запис в ексель")




    def simulationStepStarted(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step started', simTime)

        counter = 0
        normal_angle = (0, -1.5707963705062866, 0)
        normal_z = 0.088
        for spider in self.spiders:
            spider.receive_position(self.client)
            self.fitnes[counter] += 5 + \
                - abs(self.spiders[counter].get_rotation()[0] - normal_angle[0]) \
                - abs(self.spiders[counter].get_rotation()[1] - normal_angle[2]) \
                - abs(self.spiders[counter].get_rotation()[2] - normal_angle[2]) \
                - 5 * abs(self.spiders[counter].get_position()[2] - normal_z)
            self.fitnes_radical[counter] += 5 + \
                                    - 1.2 * abs(self.spiders[counter].get_rotation()[0] - normal_angle[0]) \
                                    - 1.2 * abs(self.spiders[counter].get_rotation()[1] - normal_angle[2]) \
                                    - 1.2 * abs(self.spiders[counter].get_rotation()[2] - normal_angle[2]) \
                                    - 6 * abs(self.spiders[counter].get_position()[2] - normal_z)
            print("spin", self.spiders[counter].get_rotation(), self.fitnes[counter], self.fitnes_radical[counter])

            counter += 1

    def simulationStepDone(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step done. Simulation time: ', simTime)

        for i in range(len(self.spiders)):
            self.spiders[i].move(self.client, output_data = self.neuro[i].calculate(self.spiders[i].get_all()))
        self.do_next_step = True
        self.fitnes = [0] * len(self.spiders)
        self.fitnes_radical = [0] * len(self.spiders)
        self.timer()
    def timer(self):
        self.counter += 1
        if self.counter > self.life_time:
            self.flag = False
        print(self.counter, "//", self.life_time)
