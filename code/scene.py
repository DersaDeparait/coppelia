from code.spider import Spider
from code.neuro import Neuro
from code.excel import ExcelManager
import b0RemoteApi
import time
from random import choices
import copy

class Scene:
    def __init__(self):
        self.python_client = 'b0RemoteApi_pythonClient'
        self.remote_api = 'b0RemoteApi_first'
        self.client = None

        self.do_next_step = True
        self.flag = True



        self.spiders = [  Spider(),     Spider("#0"), Spider("#1"), Spider("#2")
                         ,Spider("#3"), Spider("#4"), Spider("#5"), Spider("#6")
                         ,Spider("#7"), Spider("#8"), Spider("#9"), Spider("#10")
                         ,Spider("#11"),Spider("#12"),Spider("#13"),Spider("#14")
                        ]
        self.excel = ExcelManager(name=1, size=len(self.spiders))

        self.neuro = []
        self.neuro_father = Neuro()
        self.neuro_mother = Neuro()
        self.neuro.append(Neuro())
        self.fitnes = [0] * len(self.spiders)

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

        self.obj_hund_cube = None

        self.counter = 0
        self.life_time = 399
        self.count_of_alive = 3


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


        self.fitnes = []
        self.fitnes_radical = []
        for i in range(len(self.spiders)):
            self.fitnes.append((self.spiders[i].get_position()[1] + 10) / 20.0)
            self.fitnes_radical.append(((self.spiders[i].get_position()[1]) * 10) if ((self.spiders[i].get_position()[1]) * 10) > 0 else 0.01)
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
            self.neuro.append(Neuro.crossover_one(self.neuro_father, self.neuro_mother))
        for i in range(len(self.spiders)):
            self.spiders[i].reset_position()

    def __make_mutation(self):
        for i in range(len(self.spiders)):
            self.neuro[i].make_mutation(0.01)

    def __save_to_db(self):
        for i in range(len(self.spiders)):
            self.excel.write_data2D(i, self.fitnes[i], self.neuro[i].axon_weigh)



    def simulationStepStarted(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step started', simTime)
        for spider in self.spiders:
            spider.receive_position(self.client)

    def simulationStepDone(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step done. Simulation time: ', simTime)

        for i in range(len(self.spiders)):
            to_move = self.neuro[i].calculate(self.spiders[i].get_all())
            print(to_move)
            self.spiders[i].move(self.client, output_data =to_move)
        self.do_next_step = True
        self.timer()
    def timer(self):
        self.counter += 1
        if self.counter > self.life_time:
            self.flag = False
        print(self.counter, "//", self.life_time)
