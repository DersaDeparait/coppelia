from code.spider import Spider
from code.neuro import Neuro
from code.excel import ExcelManager
import b0RemoteApi
import time
import copy
from math import *

class Scene:
    def __init__(self):
        self.python_client = 'b0RemoteApi_pythonClient'
        self.remote_api = 'b0RemoteApi_first'
        self.client = None

        self.do_next_step = True
        self.flag = True

        self.excel = ExcelManager()

        self.spiders = [  Spider(),     Spider("#0"), Spider("#1"), Spider("#2")
                         ,Spider("#3"), Spider("#4"), Spider("#5"), Spider("#6")
                         ,Spider("#7"), Spider("#8"), Spider("#9"), Spider("#10")
                         ,Spider("#11"),Spider("#12"),Spider("#13"),Spider("#14")
                        ]
        self.neuro = []
        self.neuro.append(Neuro())

        high, weigh = self.excel.read()
        if (high != None):

            count = 0
            for i in range(len(self.neuro[0].axon_weigh)):
                to_add = count
                for j in range(len(self.neuro[0].axon_weigh[i])):
                    for k in range(len(self.neuro[0].axon_weigh[i][j])):
                        count += 1
                        self.neuro[0].axon_weigh[i][j][k] \
                            = weigh[to_add + k + j * len(self.neuro[0].axon_weigh[i][j])]

            for i in range(1, len(self.spiders)):
                if i == 1:
                    self.neuro.append(Neuro(self.neuro[0], 0.3))
                elif i == 2:
                    self.neuro.append(Neuro(self.neuro[0], 0.3))
                else:
                    self.neuro.append(Neuro(self.neuro[0], 0.1))
        else:

            for i in range(len(self.spiders)):
                self.neuro.append(Neuro())

        self.obj_hund_cube = None

        self.counter = 0
        self.life_time = 299


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

        max = 0
        for i in range(1, len(self.spiders)):
            if (self.spiders[i].get_position()[1] > self.spiders[max].get_position()[1]):
                max = i
                print(max, self.spiders[max].get_position()[1])

        neuro_best = copy.deepcopy(self.neuro[max])
        self.neuro = []
        self.neuro.append(neuro_best)
        self.spiders[0].reset_position()
        for i in range(1, len(self.spiders)):
            self.spiders[i].reset_position()
            if i == 1:
                self.neuro.append(Neuro(self.neuro[0], 0.3))
            elif i == 2:
                self.neuro.append(Neuro(self.neuro[0], 0.3))
            else:
                self.neuro.append(Neuro(self.neuro[0], 0.1))

        print("best: ", max,"//", len(self.neuro))
        for i in range(len(neuro_best.axon_weigh)):
            for j in range(len(neuro_best.axon_weigh[i])):
                print(i, j, neuro_best.axon_weigh[i][j])

        self.excel.write_data2D(self.spiders[max].get_position()[1], neuro_best.axon_weigh)


    def simulationStepStarted(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step started', simTime)
        for spider in self.spiders:
            spider.receive_position(self.client)

    def simulationStepDone(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step done. Simulation time: ', simTime)

        for i in range(len(self.spiders)):
            self.spiders[i].move(self.client, self.neuro[i].calculate(self.spiders[i].get_all()))
        self.do_next_step = True
        self.timer()
    def timer(self):
        self.counter += 1
        if self.counter > self.life_time:
            self.flag = False
        print(self.counter, "//", self.life_time)
