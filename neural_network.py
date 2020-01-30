import numpy as np
import pathlib
import os
import time
import copy


class Neuron:

    def __init__(self, numofinputs, weights=(-999,), layerName="undefined"):
        """ initialises neuron class type. weights MUST be list, not integer. If only 1 weighting of n then pass [n] """
        self.activation = tanh
        self.loss_func = mse
        self.layerName = layerName
        self.output = 0
        self.loss = 0
        self.change = 0

        if weights[0] == -999:
            self.synaptic_weights = 2 * np.random.random((numofinputs, 1)) - 1
        else:
            self.synaptic_weights = weights

    def mutate(self):  # this function randomly changes the weightings on the neuron
        for weight in self.synaptic_weights:
            weight += 0.05 * (2 * np.random.random() - 1)

    def think(self, neuron_input):
        self.output = self.activation(np.dot(neuron_input, self.synaptic_weights))
        # if self.output[0].type

    def loss(self, expected):
        self.loss = self.loss_func(self.output, expected)


# activation function being used --------------------------------------------------------------------------------------
def tanh(input):
    return np.tanh(input)


def tanh_derivative(x):
    return 1 - np.square(tanh(x))


def mse(output, expected):
    return (expected - output) ** 2

# ----------------------------------------------------------------------------------------------------------------------


class NeuralNet:
    """
        This class constitutes multi layer neural network, with variable layer sizes.
        Requires inputs of matrix of layer sizes, form [n, m, o etc]
        where num of indexes = num of layers and m, n, o etc are respective layer sizes.
        Then, weights for each if known , the name of the net and the generation number."""

    def __init__(self, layerSizes=(), firstLayerInput=1, weightsKnown=False, name=None, generation=0, projectName=None):
        """
        :param layerSizes: List or Tuple of integers holding desired layer sizes
        :param firstLayerInput: Integer representing number of inputs PER NEURON in first layer"""
        self.name = name or str(int(round(time.time() * 1000)))
        self.layers = []
        self.generation = generation
        self.fitness = 0
        self.path = ""
        self.projectName = projectName

        count = -1
        for n in range(0, len(layerSizes)):
            count += 1
            self.layers.append([""] * layerSizes[n])    # at this point, self.Layers is a list containing "", n times
            if n == 0:                                  # where n is the number of neurons in the network
                numOfInputs = firstLayerInput
            else:
                numOfInputs = layerSizes[n - 1]
            self.init_layer(self.layers[n], [weightsKnown, n], numOfInputs, ("layer_%g" %n))

    def init_layer(self, layer, loadParams, numOfInputs, layerName):  # numOfInputs is num PER NEURON not total for layer
        """ Code to initialise a layer with n neurons, where n is the number of neurons in the layer"""
        weights = list()
        # print(layer)
        if not loadParams[0]:
            weights = [[-999] * numOfInputs] * (len(layer))
        else:
            weights = self.read_weights_from_file()[loadParams[1]]

        for i in range(0, len(layer)):
            try:
                layer[i] = Neuron(numOfInputs, weights[i], layerName)
            except IndexError:
                print("INDEX ERROR LAYER %s, sub init_layer" % layerName)
            except TypeError:
                print("TYPE ERROR LAYER %s, sub init_layer" % layerName)
            except:
                print("unknown error thrown layer %s, sub init_layer" % layerName)

    def run_first_layer(self, board):
        """the first layer takes inputs in a different way to the other layers and thus requires a separate subroutine
        takes board as input. players squares should be represented as a one """

        count = 0
        for row in board:
            for square in row:
                self.layers[0][count].think(square)     # done goofed here
                count += 1                              # when reading weights in from file, missing last ??

    def feed_forward(self, layerRef=1):
        """ takes reference of the layer to pass info from [reference being with indexing starting at 1,
        so to pass info from first layer to second, layerRef = 1 etc]
        :param layerRef: reference of layer reached thus far in forward propagation. int."""

        inputs = []
        for source in self.layers[layerRef - 1]:
            try:
                inputs.append(source.output[0][0])
            except TypeError:
                print("Type Error thrown in feed_forward")
            except IndexError:
                inputs.append(source.output[0])
        inputArr = np.array(inputs)
        inputArr.transpose()
        for target in self.layers[layerRef]:
            target.think(inputArr)

    def mutate_network(self):
        """ layer1 should not be mutated as weightings must always remain zero
        This method mutates the other layers randomly

        N.B. fixed constant of mutation, contained in neuron class"""

        for layer in self.layers[1:]:
            for i in layer:
                i.mutate()

    def rtn_rating(self):
        return self.layers[-1][0].output

    def save_network(self):
        """ saves network into directory as vector """

        try:
            fLayers = open(self.path + "/layers.txt", "w")
        except FileNotFoundError:
            print("error, file at path %s not found" %str(self.path))
            return
        fLayers.write(str(len(self.layers)))
        fLayers.close()

        for i in range(0, len(self.layers)):
            fLayer = open(self.path + "/layer_%s.txt" % i, "w")

            for n in self.layers[i]:
                fLayer.write(str(n.synaptic_weights))
                fLayer.write("\n\n")
            fLayer.close()

        return 0

    def read_weights_from_file(self):
        """ reads weights from file."""

        self.path = os.path.join(os.getcwd(), self.projectName, "gen_" + str(self.generation), self.name)

        weights = []

        try:
            fLayers = open(self.path + "/layers.txt", "r")
        except OSError:
            print("error. directory %s does not exist or cannot be accessed" % self.path)
        else:
            numOfLayers = int(fLayers.read())
            fLayers.close()

            tempNeuron = []
            tempLayer = []

            for i in range(0, numOfLayers):
                fLayer = open(self.path + "/layer_%s.txt" % i, "r")

                for line in fLayer:
                    if line != "\n":
                        tempNeuron.append([float(strip_brackets_and_whitespace(line))])
                    else:
                        tempLayer.append(tempNeuron)
                        tempNeuron = []

                weights.append(tempLayer)
                tempLayer = []

        finally:
            return weights

    def mse_final_layer(self, expected):
        """ calculates loss for final layer, compared with a set of expected values,
            using the Mean Squared Error function"""

        outputs = []
        for neuron in self.layers[-1]:
            outputs.append(neuron.output)
        if len(outputs) != len(expected):
            print("error, dimensionality of expected values does not match"
                  " dimensionality of outputs in sub MSE_final_layer")
            return -1

        loss = 0
        for i in range(0, len(expected) - 1):
            loss += (expected[i] - outputs[i]) ** 2

        loss /= len(expected)
        return loss

    def make_net_dir(self):
        """ Makes new directory for Network.
        Takes path of file to save relative to, name of project, generation reference string, """

        self.path = os.path.join(os.getcwd(), self.projectName, "gen_" + str(self.generation), self.name)
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

    def backwards(self, expected):
        numOfLayers = len(self.layers) - 1
        lastLayer = True
        for i in range(numOfLayers, 0, -1):
            layer = self.layers[i]      # N.B. In python, assignment operator assigns new label to same memory ref.
            errors = list()
            if lastLayer:
                for neuron in layer:
                    neuron.change = (expected - neuron.output) * tanh_derivative(neuron.output)
                lastLayer = False
            else:
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self.layers[i + 1]:
                        error += neuron.synaptic_weights[j] * neuron.change
                    errors.append(error)
                for index, neuron in enumerate(layer):
                    neuron.change = tanh_derivative(neuron.output) * errors[index]

        return

    def backprop_layer_one(self, inputs, l_rate):
        """ This is necessary as in standard network topology, each neuron in L1 only receives one input"""
        for index, neuron in enumerate(self.layers[0]):
            neuron.synaptic_weights[0] += l_rate * neuron.change * inputs[index]

    def update_weights_backprop(self, inputs, l_rate):
        for index, layer in enumerate(self.layers):
            if index != 0:
                inputs = [neuron.output for neuron in self.layers[index-1]]
                for neuron in layer:
                    for i in range(len(neuron.synaptic_weights)):
                        # print(i)
                        # print(neuron.change)
                        # print(inputs[i])
                        # print(neuron.synaptic_weights)
                        neuron.synaptic_weights[i][0] += l_rate * neuron.change * inputs[i]
            else:
                self.backprop_layer_one(inputs, l_rate)

########################################################################################################################


def strip_brackets_and_whitespace(input):
    return input.rstrip().replace('[', '').replace(']', '')


########################################################################################################################


def rank_generation(networks):
    """ sort list of generations by score. currently uses bubble so change this
    :param networks: as list of network objects
    :return networks: as sorted list"""
    try:
        hold = networks[0]
    except IndexError:
        print("rank_generation failed as ")

    inOrder = False
    n = len(networks) - 1
    while not inOrder and n != 1:
        for x in range(0, n):
            inOrder = True
            if networks[x].fitness > networks[x + 1].fitness:
                networks[x + 1], networks[x] = networks[x], networks[x + 1]
                inOrder = False
        n -= 1
    return networks


def save_generation(networks):
    """ save all networks to relevant directories.
     :param networks: array of instances of network class"""
    for network in networks:
        if not isinstance(network, NeuralNet):
            print("Item not NeuralNet type")
            continue
        try:
            network.make_net_dir()
        except "Directory Access Failure":
            print("could not make directory at path %s" % network.path)
        else:
            print("successfully made directory as path %s" % network.path)
            try:
                network.save_network()
            except "Directory Access Failure":
                print("could not write to directory %s" % network.path)

    return 0


def mutate_and_update(networks):
    i = 0
    for network in networks:
        if not isinstance(network, NeuralNet):
            print("Error, 'networks' may only contain instances of network class")
            continue


        network.mutate_network()
        network.fitness = 0
        network.generation += 1
        i += 1

    return 0


def save_meta_data(data_to_save=(("no data passed", 0)), networks=()):
    """ save metadata of generation into meta.txt file in generation folder
    :param data_to_save: Tuple of tuples, each containing parameter name / parameter
                         eg. ("max fitness", 100)
    :param networks: list or list-like object of instances of network class"""
    try:
        metaPath = networks[0].path.replace(networks[0].name, "meta.txt")
    except IndexError:
        print("networks cannot be empty, sub save_meta_data")
        return
    except AttributeError:
        print("networks must contain instance of network class, sub save_meta_data")
        return
    except:
        print("unknown error, sub save_meta_data")
        return

    try:
        fMeta = open(metaPath, 'w')
    except PermissionError:
        print("file at %s cannot be accessed due to permissions" % metaPath)
        return

    if not data_to_save[0]:
        print("no data to save")
        return

    for pairing in data_to_save:
        fMeta.write("%s : %s" % (str(pairing[0]), str(pairing[1])))

    fMeta.close()
    return


def eliminate_bottom_networks(networks):
    """ removes bottom half of table of networks and replaces them with the corresponding upper ones """

    for i in range(0, int(len(networks) / 2)):
        networks[-(i + 1)] = copy.deepcopy(networks[i])
        networks[-(i + 1)].name = str(int(round(time.time() * 1000)))

########################################################################################################################
########################################################################################################################


if __name__ == "__main__":
    # net = neural_net([64, 42, 1], False, "1564341349747", 2, "opti_reversi")
    # test = "test"
    pass
