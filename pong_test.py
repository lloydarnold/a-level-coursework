import pong_ai_v3 as pong
import neural_network as nn


def test_init_board():
    print("Test init screen function")
    screen = pong.init_screen()
    del screen
    print("\n")


def test_init_game_objects():
    print("Test object creation and object draw methods")
    screen = pong.init_screen()
    ball, bat1, bat2 = pong.init_game_objects(screen)
    print("Ball object : " + str(ball))
    print("Bat object 1 : " + str(bat1))
    print("Bat object 2 : " + str(bat2))
    del ball
    del bat1
    del bat2


def test_update():
    print("test update_net_weightings sub")
    net = nn.NeuralNet((6, 40, 20, 1), 1, False, "grad_descent_net", 0, pong.PROJECT_NAME)
    print("Weighting 2,0,0 before: %g " % net.layers[2][0].synaptic_weights[0])
    print("Weighting 1,0,0 before: %g " % net.layers[1][0].synaptic_weights[0])
    print("Weighting 0,1,0 before: %g " % net.layers[0][1].synaptic_weights[0])

    inputArr, outputArr, expectedArr = pong.read_record_data(1)
    pong.update_net_weightings(net, inputArr, expectedArr)
    print("\n")
    print("Weighting 2,0,0 after: %g " % net.layers[2][0].synaptic_weights[0])
    print("Weighting 1,0,0 after: %g " % net.layers[1][0].synaptic_weights[0])
    print("Weighting 0,1,0 after: %g " % net.layers[0][1].synaptic_weights[0])

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


def test_save_record_data():
    print("testing save record data function")
    data = (([70, 70, 10, 180, 5, 5],-0.979104,1.000000),
    ( [85, 85, 10, 200, 5, 5],-0.979104,1.000000),
    ( [90, 90, 10, 220, 5, 5],-0.979104,1.000000),
    ( [95, 95, 10, 240, 5, 5],-0.979104,1.000000))

    pong.save_record_data(data, 999)
    print("\n")


def test_read_record_data():
    print("testing read record data function")
    inputArr, outputArr, expectedArr = pong.read_record_data(999)
    print("File read succesfully, contents: \n")
    for i, input in enumerate(inputArr):
        print("Input: %g, Output: %g, Expected: %g " % (input, outputArr[i], expectedArr[i]))
    print("\n")


if __name__ == "__main__":
    test_init_board()
    test_init_game_objects()
    test_update()
    test_run_game()
    test_save_record_data()
    test_save_record_data()
    test_read_record_data()
