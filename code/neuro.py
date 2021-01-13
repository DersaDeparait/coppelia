import code.config as config
import random
import math
import copy

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


class Web:
    def __init__(self, layers = config.WEB_LAYERS, web = None, randomize = None):
        self.layers = layers
        self.activation_function = lambda number: number
        if web != None:
            self.layers = copy.copy(web.layers)
            self.neurons = [[web.neurons[i][j] for j in range(self.layers[i])] for i in range(len(self.layers))]
            self.axon_weigh = [[web.axon_weigh[i][j] for j in range(self.layers[i] * self.layers[i + 1])] for i in range(len(self.layers) - 1)]
            self.axon_bias = [web.axon_bias[i] for i in range(len(web.axon_bias))]
        else:
            self.neurons = [[0 for j in range(self.layers[i])] for i in range(len(self.layers))]
            self.axon_weigh = [[0 for j in range(self.layers[i] * self.layers[i + 1])] for i in range(len(self.layers) - 1)]
            self.axon_bias = [0 for i in range(len(self.layers) - 1)]
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



    def cross_crossover_one(self, neuro_1):
        new_neuro = Web(web = self)
        sum = 0
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                sum += 1
            sum += 1

        point = random.randint(0, sum - 1)
        counter = 0
        if random.random()<0.5:
            for i in range(len(new_neuro.axon_weigh)):
                for j in range(len(new_neuro.axon_weigh[i])):
                    if counter > point:
                        new_neuro.axon_weigh[i][j] = neuro_1.axon_weigh[i][j]
                    counter += 1
                if counter > point:
                    new_neuro.axon_bias[i] = neuro_1.axon_bias[i]
                counter += 1
        else:
            for i in range(len(new_neuro.axon_weigh)):
                for j in range(len(new_neuro.axon_weigh[i])):
                    if counter < point:
                        new_neuro.axon_weigh[i][j] = neuro_1.axon_weigh[i][j]
                    counter += 1
                if counter < point:
                    new_neuro.axon_bias[i] = neuro_1.axon_bias[i]
                counter += 1
        return new_neuro
    def cross_crossover_several(self, neuro_1, point_number : int = 2):
        if point_number < 1: point_number = 1

        new_neuro = Web(web = self)
        sum = 0
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                sum += 1
            sum += 1
        if point_number >= sum: point_number = sum

        possible_points = [i for i in range(sum)]
        points = []
        for i in range(point_number):
            number = random.choice(possible_points)
            points.append(number)
            possible_points.remove(number)

        points.sort()

        start_parent = random.choice([False, True])

        counter = 0
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                if len(points) > 0 and counter > points[0]:
                    start_parent = not start_parent
                    points.pop(0)
                if start_parent:
                    new_neuro.axon_weigh[i][j] = neuro_1.axon_weigh[i][j]
                counter += 1
            if len(points) > 0 and counter > points[0]:
                start_parent = not start_parent
                points.pop(0)
            if start_parent:
                new_neuro.axon_bias[i] = neuro_1.axon_bias[i]
            counter += 1
        return new_neuro

    def cross_randomize(self, neuro_1):
        new_neuro = Web(web = self)
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                if random.random() < 0.5:
                    new_neuro.axon_weigh[i][j] = neuro_1.axon_weigh[i][j]
            if random.random() < 0.5:
                new_neuro.axon_bias[i] = neuro_1.axon_bias[i]
        return new_neuro
    def cross_average(self, neuro_1):
        new_neuro = Web(web=self)
        for i in range(len(new_neuro.axon_weigh)):
            for j in range(len(new_neuro.axon_weigh[i])):
                new_neuro.axon_weigh[i][j] = random.uniform(new_neuro.axon_weigh[i][j], neuro_1.axon_weigh[i][j])
            new_neuro.axon_bias[i] = random.uniform(new_neuro.axon_bias[i], neuro_1.axon_bias[i])
        return new_neuro

    # cross_crossover_multi_several, cross_crossover_cycle
    # cross_lineral, cross_discret, cross_interjacent
    # fitnes

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

web = Web(layers=[2, 3, 2])
web.axon_weigh = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
web.axon_bias = [13, 14]
# web.set_function(lambda number: math.tanh(number))
print("father", web.axon_weigh, web.axon_bias)

webM = Web(layers = [2, 3, 2])
webM.axon_weigh = [[-1, -2, -3, -4, -5, -6], [-7, -8, -9, -10, -11, -12]]
webM.axon_bias = [-13, -14]
print("mother", webM.axon_weigh, webM.axon_bias)

for i in range(1000):
    child = webM.cross_crossover_several(web, 4)
    print("child {}".format(i), child.axon_weigh, child.axon_bias)