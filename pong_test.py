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
    inputArr, outputArr, expectedArr = pong.read_record_data(1)

    pong.update_net_weightings(net, inputArr, expectedArr)
    print("")


if __name__ == "__main__":
    test_init_board()
