from code.character import Character
from code.spider import Spider
from code.neuro import Neuro
from code.excel import ExcelManager
import b0RemoteApi
import code.config as config
import time
from random import choices
import random

class Scene:
    def __init__(self):
        self.__set_connetcion_variables_to_lib_files()

        self.__create_spiders()
        self.__create_or_connect_to_file()
        self.__create_neuro()
        self.__set_parameters_of_neuro()

        self.__set_parameters_for_loop_work()
    def __set_connetcion_variables_to_lib_files(self):
        self.python_client = 'b0RemoteApi_pythonClient'
        self.remote_api = 'b0RemoteApi_first'
        self.client = None
    def __create_spiders(self):
        self.characters = []
        for i in range(config.NUMBER_OF_SPIDERS):
            self.characters.append(Character())

        self.spiders = [Spider()]
        for i in range(1, config.NUMBER_OF_SPIDERS):
            self.spiders.append(Spider("#{}".format(i - 1)))
    def __create_or_connect_to_file(self):
        self.excel = ExcelManager(name=config.FILE_NAME, size=len(self.spiders))
        self.excel = CscManager(name=config.FILE_NAME, size=len(self.spiders))
    def __create_neuro(self):
        self.neuro = []
        self.neuro_father = Neuro()
        self.neuro_mother = Neuro()
        self.neuro.append(Neuro())
        self.fitnes = [0] * len(self.spiders)
        self.fitnes_radical = [0] * len(self.spiders)

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
    def __set_parameters_of_neuro(self):
        self.life_time = config.CYCLE_TIME
        self.count_of_alive = config.COUNT_OF_ALIVE
        self.mutation_power = config.MUTATION_POWER
    def __set_parameters_for_loop_work(self):
        self.do_next_step = True
        self.flag = True
        self.counter = 0



    def start(self):
        while True:
            with b0RemoteApi.RemoteApiClient(self.python_client, self.remote_api) as self.client:
                self.__add_method()
                self.__add_objects()
                self.__start_simulation()

                self.__loop()

                self.__finish_simulation()
                self.__remake_neural_network()
            time.sleep(1)

    def __add_method(self):
        self.client.simxSynchronous(True)
        self.client.simxGetSimulationStepStarted(self.client.simxDefaultSubscriber(self.simulationStepStarted))
        self.client.simxGetSimulationStepDone(self.client.simxDefaultSubscriber(self.simulationStepDone))
    def __add_objects(self):
        #err_hand_cube, self.obj_hund_cube = self.client.simxGetObjectHandle('Cuboid', self.client.simxServiceCall())
        for spider in self.spiders:
            spider.set_robot(self.client)
    def __start_simulation(self):
        self.client.simxStartSimulation(self.client.simxDefaultPublisher())
    def __loop(self):
        while self.flag:
            if self.do_next_step:
                self.do_next_step = False
                self.client.simxSynchronousTrigger()
            self.client.simxSpinOnce()
    def __finish_simulation(self):
        self.client.simxStopSimulation(self.client.simxDefaultPublisher())
    def __remake_neural_network(self):
        self.remake_neural()




    def remake_neural(self):
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
        for i in range(self.count_of_alive - 1):
            else_number = choices(index, weights = self.fitnes_radical, k = 1)[0]
            while else_number in self.alive:
                print("Same {}".format(else_number))
                else_number = choices(index, weights=self.fitnes_radical, k=1)[0]
                print("new {}, all {}".format(else_number, self.alive))
            self.alive.append(else_number)
    def __make_new_population(self):
        neuro_new = []
        for i in range(self.count_of_alive):
            neuro_new.append(self.neuro[self.alive[i]])
        self.neuro = neuro_new
        for i in range(self.count_of_alive, len(self.spiders)):
            if random.random() > 0.5:
                self.neuro.append(Neuro.randomize_new(self.neuro_father, self.neuro_mother))
            else:
                self.neuro.append(Neuro.randomize_new(self.neuro_mother, self.neuro_father))
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
            self.spiders[i].move(self.client, output_data = self.neuro[i]._calculate(self.spiders[i].get_all()))
        self.do_next_step = True
        self.fitnes = [0] * len(self.spiders)
        self.fitnes_radical = [0] * len(self.spiders)
        self.__timer()
    def __timer(self):
        self.counter += 1
        if self.counter > self.life_time:
            self.flag = False
        print(self.counter, "//", self.life_time)
