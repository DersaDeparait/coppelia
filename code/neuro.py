import random
import math

class Neuro:
    def __init__(self, neuro = None, mutant_power = 0):
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
                        self.axon_weigh[i][j].append(random.uniform(-1, 1))

    def crossover_one(neuro_0, neuro_1):
        new_neuro = Neuro(neuro_0)
        sum = 0
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                for k in range(len(new_neuro.axon_weigh[i])):
                    sum += 1
        point = random.randint(1, sum)
        counter = 0
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                for k in range(len(new_neuro.axon_weigh[i][j])):
                    if counter > point:
                        new_neuro.axon_weigh[i][j][k] = neuro_1.axon_weigh[i][j][k]
                    counter += 1
        return new_neuro

    def randomize_new(neuro_0, neuro_1):
        new_neuro = Neuro(neuro_0)
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                for k in range(len(new_neuro.axon_weigh[i][j])):
                    if random.random() < 0.5:
                        new_neuro.axon_weigh[i][j][k] = neuro_1.axon_weigh[i][j][k]
        return new_neuro

    def make_mutation(self, percent):
        dispers = 0
        counter = 0
        for i in range(len(self.axon_weigh)):
            for j in range(len(self.axon_weigh[i])):
                for k in range(len(self.axon_weigh[i][j])):
                    dispers += self.axon_weigh[i][j][k]
                    counter+=1
        dispers = dispers / counter + 0.1
        for i in range(len(self.axon_weigh)):
            for j in range(len(self.axon_weigh[i])):
                for k in range(len(self.axon_weigh[i][j])):
                    if random.random() < percent:
                        self.axon_weigh[i][j][k] += random.uniform(-dispers, dispers)

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
