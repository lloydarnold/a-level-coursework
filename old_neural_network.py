import numpy as np
import pathlib, os, time


class Neuron:

    def __init__(self, numofinputs, weights=[-999], layerName="undefined"):
        """ initialises neuron class type. weights MUST be list, not integer. If only 1 weighting of n then pass [n] """
        self.activation = tanh
        self.layerName = layerName
        self.output = 0
        if weights[0] == -999:
            seed = gen_random_seed()
            np.random.seed()
            self.synaptic_weights = 2 * np.random.random((numofinputs, 1)) - 1
        else:
            self.synaptic_weights = weights
        # self.output = []
        true = True

    def mutate(self):  # this function randomly changes the weightings on the neuron
        for weight in self.synaptic_weights:
            weight = weight + 0.05 * (2 * np.random.random() - 1)

    # alternative way of thinking that stores output as object property:
    def think(self, input):
        self.output = self.activation(np.dot(input, self.synaptic_weights))

# activation function being used ---------------------------------------------------------------------------------------------------------------------------------------------
def tanh(input):
    return (np.tanh(input))


def tanh_derivative(x):
    return (1 - np.square(tanh(x)))


def gen_random_seed():
    return int(round(time.time() * 100) / 200) - np.random.rand(0, 1000)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class NeuralNet:
    """ This class constitutes multi layer neural network, with variable layer sizes. This translates into one input layer, one output layer and n hidden layers
        Requires inputs of matrix of layer sizes, form [n, m, o etc] where sum m,n,o = num of layers and m, n and o are respective layer sizes.
        Then, weights for each if known , the name of the net and the generation number.

        Passing -999 * layersize will generate weights randomly."""

    def __init__(self, layers=[], weights=[[], [], []], name=None, generation=0):
        self.name = name or str(int(round(time.time() * 1000)))
        self.layers = []
        self.generation = generation
        self.score = 0
        self.path = ""

        count = -1
        for n in range(0, len(layers)):
            count += 1
            self.layers.append([""] * layers[n])
            if n == 0:
                numOfInputs = layers[0]
            else:
                numOfInputs = layers[n - 1]
            self.init_layer(self.layers[n], weights[n], numOfInputs)

    def init_layer(self, layer, weights, numOfInputs):  # numOfInputs is num PER NEURON not total for layer
        if weights == []:
            weights.append(0) * len(layer)  # <-----------------------------------------
        for i in range(0, len(layer)):  # <----------------------------------------- HERE NEEDS WORK
            layer[i] = Neuron(numOfInputs, weights[0][i])  # <-----------------------------------------

    def run_first_layer(self, board):
        """the first layer takes inputs in a different way to the other layers and thus requires a seperate subroutine
        takes board as input. players squares should be represented as a one """

        count = 0
        for row in board:
            for square in row:
                self.layers[0][count].think(square)
                count += 1

    def feed_forward(self, layerRef=1):
        """ takes reference of the layer to pass info from [reference being with indexing starting at 1,
        so to pass info from first layer to second, layerRef = 1 etc]"""
        inputs = []
        for source in self.layers[layerRef - 1]:
            inputs.append(source.output)
        for target in self.layers[layerRef]:
            target.think(inputs)

    def mutate_network(self):
        """ layer1 should not be mutated as weightings must always remain zero
        This method mutates the other two layers randomly"""

        for layer in self.layers[1:]:
            for i in layer:
                i.mutate()

    def rtn_rating(self):
        return self.layers[-1][0].output

    def save_network(self):
        """ saves network into directory set """

        fLayers = open(self.path + "/layers.txt", "w")
        fLayers.write(str(len(self.layers)))
        fLayers.close()

        for i in range(0, len(self.layers)):
            fLayer = open(self.path + "/layer_%s.txt" % i, "w")

            for n in self.layers[i]:
                fLayer.write(str(n.synaptic_weights))
                fLayer.write("\n\n")
            fLayer.close()

        return 0

    def read_weights_from_file(self, projectName):
        """ reads weights from file, needs projectName parameter. rest of file path is derived from self data."""

        fLayers = open(self.path + "/layers.txt", "r")
        numOfLayers = int(fLayers.read())
        fLayers.close()

        weights = []
        tempNeuron = []
        tempLayer = []

        for i in range(0, numOfLayers):
            fLayer = open(self.path + "/layer_%s.txt" % i, "r")

            for line in fLayer:
                if line != "\n":
                    tempNeuron.append(float(strip_brackets_and_whitespace(line)))
                else:
                    tempLayer.append(tempNeuron)
                    tempNeuron = []

            weights.append(tempLayer)
            tempLayer = []

        return weights

    def make_net_dir(self, projectName):
        """ Makes new directory for Network.
        Takes path of file to save relative to, name of project, generation reference string, """

        self.path = os.path.join(os.getcwd(), projectName, "gen_" + str(self.generation), self.name)
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)


#########################################################################################################################################

def strip_brackets_and_whitespace(input):
    return input.rstrip().replace('[', '').replace(']', '')


def load_network(projectName, generation, name):
    """ loads network from a file. """
    networkPath = os.path.join(os.cwd(), projectName, generation, name)

    ############### to this point, return

    return 1