import time
from datetime import datetime

import b0RemoteApi

from code.csv_manager import CscManager
from code.excel import ExcelManager
from code.character import Character
import code.config as code_config

class Scene:
    def __init__(self):
        self.__init_log()
        self.__init_coppelia()
        self.__init_loop_params()
        self.__init_config()
        self.__init_create_spiders()
        self.__init_read_from_file()
    def __init_log(self):
        self.show_info = code_config.SHOW_INFO  # Виводить в консоль дані
        self.time_start = datetime.now()
        self.time_last_print = datetime.now()
        self.time_after_beggining = 0
        self.time_after_last_print = 0
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
        self.character = []
        for i in range(self.number_of_spiders):
            self.character.append(Character())
    def __init_read_from_file(self):
        self.csv = CscManager(code_config.FILE_NAME)
        self.csv2 = CscManager(1000 + code_config.FILE_NAME)
        # high, weigh = self.excel.read(0)
        # if (high != None):
        #
        #     count = 0
        #     for i in range(len(self.web[0].axon_weigh)):
        #         to_add = count
        #         for j in range(len(self.web[0].axon_weigh[i])):
        #             for k in range(len(self.web[0].axon_weigh[i][j])):
        #                 count += 1
        #                 self.web[0].axon_weigh[i][j][k] \
        #                     = weigh[to_add + k + j * len(self.web[0].axon_weigh[i][j])]
        #
        #     for w in range(1, len(self.spiders)):
        #         high, weigh = self.excel.read(w)
        #         self.web.append(Neuro())
        #         count = 0
        #         for i in range(len(self.web[w].axon_weigh)):
        #             to_add = count
        #             for j in range(len(self.web[w].axon_weigh[i])):
        #                 for k in range(len(self.web[w].axon_weigh[i][j])):
        #                     count += 1
        #                     self.web[w].axon_weigh[i][j][k] \
        #                         = weigh[to_add + k + j * len(self.web[w].axon_weigh[i][j])]
        # else:
        #     for i in range(1, len(self.spiders)):
        #         self.web.append(Neuro(mutant_power=1))


    def _print_time(self, message = ""):
        if self.show_info:
            self.time_after_beggining = datetime.now() - self.time_start
            self.time_after_last_print = datetime.now() - self.time_last_print
            self.time_last_print = datetime.now()
            print("------- {0}  -  {1}  -  {2}  ---------------------------------"
                  .format(self.time_after_last_print, self.time_after_beggining, message))
            print()


    def start(self):
        while True:
            self._print_time("Нова епоха: {}".format(self.epoch))
            with b0RemoteApi.RemoteApiClient(self.python_client, self.remote_api) as self.client:
                self._print_time("Підключилося до копелії")
                self.__add_method()
                self._print_time("Додано методи")
                self.__add_objects()
                self._print_time("Додано обєкти")
                self.__start_simulation()
                self._print_time("Почалася симуляція")

                self.client.simxSetBoolParameter(
                    b'sim.boolparam_display_enabled',
                    False,
                    self.client.simxDefaultPublisher()
                )
                self.client.simxSetIntParameter(
                    b'sim.intparam_speedmodifier',
                    6,
                    self.client.simxDefaultPublisher()
                )
                self.__loop()
                self._print_time("Закінчився основний цикл")
                self.__finish_simulation()
                self._print_time("Зкнічили симуляцію")
                self.__remake_neural_network()
                self._print_time("Переробили нейронку")
            self._print_time("Вийшли із роботи із підєднанням")
            time.sleep(1)
            self._print_time("Завершили епоху")
            self.epoch += 1
    def __add_method(self):
        self.client.simxSynchronous(True)
        self.client.simxGetSimulationStepStarted(self.client.simxDefaultSubscriber(self.simulationStepStarted))
        self.client.simxGetSimulationStepDone(self.client.simxDefaultSubscriber(self.simulationStepDone))
    def __add_objects(self):
        #err_hand_cube, self.obj_hund_cube = self.client.simxGetObjectHandle('Cuboid', self.client.simxServiceCall())
        for i in range(len(self.character)):
            self.character[i].connect_robot(self.client)
            self._print_time("Завершено робот {}".format(i))
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
        self.remake_neural_network()


    def simulationStepStarted(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step started', simTime)
        pass
    def simulationStepDone(self, msg):
        #simTime = msg[1][b'simulationTime']
        #print('Simulation step done. Simulation time: ', simTime)
        for i in range(len(self.character)):
            self.character[i].iteration_done(self.client)
        self.do_next_step = True
        self.__add_counter()
    def __add_counter(self):
        self._print_time("{}/{}".format(self.counter,self.life_time))
        self.counter += 1
        if self.counter > self.life_time:
            self.flag = False



    def remake_neural_network(self):
        self.counter = 0
        self.flag = True

        for i in range(len(self.character)):
            self.character[i].do_end_of_epoch()

        Character.calculate_all()

        self.__save_to_db()
        for i in range(len(self.character)):
            self.character[i].reset_fitnes()

    def __save_to_db(self):
        self.csv.extend_row_by_dicts(map = Character.save_to_db_fitnes())
        self.csv2.set_data_by_dicts(Character.save_to_db_last_web())
        self.csv.write()
        self.csv2.write()
