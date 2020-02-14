import pong_ai_v3 as pong
import neural_network as nn


def test_init_board():
    print("Test init screen function")
    screen = pong.init_screen()
    del screen
    print("\n")


def test_update():
    print("test update_net_weightings sub")
    net = nn.NeuralNet((6, 40, 20, 1), 1, False, "grad_descent_net", 0, pong.PROJECT_NAME)
    print("Weighting 1,0,0 before: %g " % net.layers[1][0].synaptic_weights[0])
    inputArr, outputArr, expectedArr = pong.read_record_data(1)
    pong.update_net_weightings(net, inputArr, expectedArr)
    print("Weighting 1,0,0 after: %g " % net.layers[1][0].synaptic_weights[0])
    print("\n")
    del net


def test_run_game():
    print("testing base gameplay function (from pong_AI_v3) ")
    screen = pong.init_screen()
    net = nn.NeuralNet((6, 40, 20, 1), 1, False, "grad_descent_net", 0, pong.PROJECT_NAME)
    pong.run_game(screen, net)
    del screen
    del net
    print("gameplay successful")


if __name__ == "__main__":
    test_init_board()
    test_update()
