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


import random
import code.config as config

class Web:
    def __init__(self, layers = config.WEB_LAYERS, web = None, randomize = None):
        self.layers = layers
        self.activation_function = lambda number: number
        if web != None:
            self.neurons = [[web.neurons[i][j] for j in range(layers[i])] for i in range(len(layers))]
            self.axon_weigh = [[web.axon_weigh[i][j] for j in range(layers[i] * layers[i + 1])] for i in range(len(layers) - 1)]
            self.axon_bias = [web.axon_bias[i] for i in range(len(web.axon_bias))]
        else:
            self.neurons = [[0 for j in range(layers[i])] for i in range(len(layers))]
            self.axon_weigh = [[0 for j in range(layers[i] * layers[i + 1])] for i in range(len(layers) - 1)]
            self.axon_bias = [0 for i in range(len(layers) - 1)]
        if randomize != None: self.randomize(randomize)



    def randomize(self, size = 0.01):
        for i in range(len(self.axon_weigh)):
            for j in range(len(self.axon_weigh[i])):
                self.axon_weigh[i][j] += random.uniform(-size, size)
    def make_mutation(self, percent = config.MUTATION_POWER, power = 1.):
        dispers = 0 + (sum(self.axon_bias))
        counter = 0 + len(self.axon_bias)
        for i in range(len(self.axon_weigh)):
            for j in range(len(self.axon_weigh[i])):
                dispers += self.axon_weigh[i][j]
                counter += 1
        dispers = dispers / counter + 0.1
        for i in range(len(self.axon_weigh)):
            for j in range(len(self.axon_weigh[i])):
                if random.random() < percent:
                    self.axon_weigh[i][j] += random.uniform(-dispers * power, dispers * power)
        for i in range(len(self.axon_bias)):
            if random.random() < percent:
                self.axon_bias[i] += random.uniform(-dispers * power, dispers * power)
    def new_randomize_deep_copy(self, size = 0.1):
        return Web(self.layers, web = self, randomize= size)
    def new_mutant_deep_copy(self, percent = config.MUTATION_POWER, power = 1.):
        web = Web(self.layers, web = self)
        web.make_mutation(percent = percent, power = power)
        return web



    def set_function(self, activation_function):
        self.activation_function = activation_function


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


    def calculate_all(self, input):
        self._set_input(input)
        self._calculate()
        return self._get_output()
    def _set_input(self, input):
        for i in range(len(self.neurons[0])):
            self.neurons[0][i] = input[i]
    def _calculate(self):
        for i in range(1, len(self.neurons)):
            for j in range(len(self.neurons[i])):
                sum = 0
                for k in range(len(self.neurons[i - 1])):
                    sum += self.axon_weigh[i - 1][k * len(self.neurons[i]) + j] * self.neurons[i - 1][k]
                sum = sum + self.axon_bias[i - 1]
                self.neurons[i][j] = self.activation_function(sum)
    def _get_output(self):
        return self.neurons[-1]

web = Web(layers=[2, 3, 2], randomize = 1)
web.axon_weigh = [[1, 1, 1, 1, 1, -1], [1, 2, -1, 0, 1, 1]]
web.axon_bias = [1, -1]
# web.set_function(lambda number: math.tanh(number))
print("neuron", web.neurons)
print("axon", web.axon_weigh)
print("bias",  web.axon_bias)
print("result:", web.calculate_all([1, 1]))
print("neuron", web.neurons)

w = web.new_mutant_deep_copy(0.5, 10)
print("axon", web.axon_weigh)
print("axon", w.axon_weigh)
print("bias",  web.axon_bias)
print("bias",  w.axon_bias)
