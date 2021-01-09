import random
import math

class Neuro:
    def __init__(self, neuro = None, mutant_power = 0.1):
        self.input_data = []
        self.output_data = []

        self.layers = [18, 18, 18, 18]#[24, 3]

        self.axon_weigh = []
        for i in range(len(self.layers) - 1):
            self.axon_weigh.append([])
            for j in range(self.layers[i] + 1):
                self.axon_weigh[i].append([])
                for k in range(self.layers[i+1]):
                    if neuro != None:
                        self.axon_weigh[i][j].append(neuro.axon_weigh[i][j][k] + random.uniform(-mutant_power, mutant_power))
                    else:
                        self.axon_weigh[i][j].append(random.uniform(-0.7, 0.7))

    def calculate(self, input_data, layer_number = 0):
        if (layer_number >= len(self.layers) - 1):
            return input_data
        else:
            input_data.append(1.)
            self.output_data = []
            for j in range(self.layers[layer_number + 1]):
                sum = 0
                for i in range(len(input_data)):
                    sum += input_data[i] * self.axon_weigh[layer_number][i][j]
                self.output_data.append(self._activation(sum))

            return self.calculate(self.output_data, layer_number + 1)

    def _activation(self, number):
        return math.tanh(number)