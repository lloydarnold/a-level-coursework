import neural_network as nn


def test_neuron_init():
    print("testing neuron initialisation ")
    neuron = nn.Neuron(5, [-999] * 5, "test_layer")
    print("neuron: " + str(neuron))
    print("neuron layer: %s " % neuron.layerName)
    print("weighting 0: %s " % neuron.synaptic_weights[0])
    print("\n")
    del neuron


def test_neuron_mutate():
    print("testing neuron mutation ")
    neuron = nn.Neuron(5, [-999] * 5)
    print("neuron: " + str(neuron))
    print("weighting 0 before mutation: %s " % neuron.synaptic_weights[0])
    neuron.mutate()
    print("weighting 0 after mutation : %s " % neuron.synaptic_weights[0])
    print("\n")
    del neuron


def test_neuron_think():
    print("testing neuron think with two inputs ")
    neuron = nn.Neuron(2, [-999] * 2)
    print("neuron: " + str(neuron))
    inputs = [1, -1]
    print("inputs = %s " % str(inputs))
    neuron.think(inputs)
    print("output = %g " % neuron.output)
    print("\n")
    del neuron


def test_neuron_loss():
    print("testing neuron loss ")
    neuron = nn.Neuron(2, [-999] * 2)
    print("neuron: " + str(neuron))
    inputs = [1, -1]
    expected = -1
    neuron.think(inputs)
    neuron.calc_loss(expected)
    print("inputs = %s " % str(inputs))
    print("output = %g " % neuron.output)
    print("expected = %s " % expected)
    print("loss = %g " % neuron.loss)
    print("\n")
    del neuron


def test_net_init():
    print("Testing network initialisation ")
    net = nn.NeuralNet([64, 42, 1], 1, False, "test_name", 1, "test_project")
    print("network: " + str(net))
    print("network name: %s " % net.name)
    print("project name: %s " % net.projectName)
    print("\n")
    del net


if __name__ == "__main__":
    test_neuron_init()
    test_neuron_mutate()
    test_neuron_think()
    test_neuron_loss()
    test_net_init()
