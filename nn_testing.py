import neural_network as nn


def test_net_init():
    print("Testing network initialisation ")
    net = nn.NeuralNet([64, 42, 1], 1, False, "test_name", 1, "test_project")
    print("network: " + str(net))
    print("network name: %s " % net.name)
    print("project name: %s " % net.projectName)
    print("\n")



def test_neuron_init():
        print("Testing neuron initialisation ")
        neuron = nn.Neuron(5, [-999] * 5, "test_layer")
        print("neuron: " + str(neuron))
        print("neuron layer: %s " % neuron.layerName)
        print("weighting 0: %s " % neuron.synaptic_weights[0])
        print("\n")


if __name__ == "__main__":
    test_neuron_init()
    test_net_init()
