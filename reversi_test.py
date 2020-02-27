import reversi_ai_v2 as rev
import random
import neural_network as nn


def test_init_grid():
    print("testing init_grid sub")
    grid = rev.initiate_grid()
    for row in grid:
        print(str(row))
    del grid
    print("\n")

def test_check_legal():
    print("testing check_legal subroutine with legal move (5,3) for player -1 as first move ")
    grid = rev.initiate_grid()
    print("Returns: %s" % str(rev.check_legal(grid, 5, 3, -1, [0, -1])))
    print("testing check_legal subroutine with illegal move (4,4) for player -1 as first move ")
    print("Returns: %s" % str(rev.check_legal(grid, 4, 4, -1, [0, -1])))
    print("testing check_legal subroutine with illegal move (5,5) for player -1 as first move ")
    print("Returns: %s" % str(rev.check_legal(grid, 5, 5, -1, [0, -1])))
    print("\n")

def test_legal_moves():
    print("testing subroutine to find legal moves available")
    grid = rev.initiate_grid()
    moves = rev.legal_moves(grid, -1)
    for move in moves:
        print(move[0])
    print("\n")


def test_merge_sort():
    print("testing merge sort method")
    nets = rev.init_networks(10)
    for net in nets:
        net.fitness = random.randint(0, 100)
    nets = rev.mergesort(nets)
    for net in nets:
        print(net.fitness)


def test_pick_move_nn():
    print("testing pick move with neural network function")
    net = nn.NeuralNet([64, 42, 1], 1, False, "test_network", "test_project")
    grid = rev.initiate_grid()
    moves = rev.legal_moves(grid, -1)
    bestMove = rev.eval_move_with_neural_net(grid, moves, -1, net)
    print("first test. best move according to network 1 is: %s " % str(bestMove[0]) )
    bestMove = rev.eval_move_with_neural_net(grid, moves, -1, net)
    print("second test. best move according to network 1 is: %s" % str(bestMove[0]))
    del net
    net = nn.NeuralNet([64, 42, 1], 1, False, "test_network", "test_project")
    bestMove = rev.eval_move_with_neural_net(grid, moves, -1, net)
    print("first test. best move according to network 2 is: %s " % str(bestMove[0]) )
    bestMove = rev.eval_move_with_neural_net(grid, moves, -1, net)
    print("second test. best move according to network 2 is: %s" % str(bestMove[0]))
    del net
    print("\n")


def test_pick_rand_move():
    print("testing pick random move function")
    grid = rev.initiate_grid()
    moves = rev.legal_moves(grid, -1)
    bestMove = rev.pick_random_move(moves)
    print("first test. best move according to random is: %s " % str(bestMove[0]) )
    bestMove = rev.pick_random_move(moves)
    print("second test. best move according to random is: %s " % str(bestMove[0]) )
    print("\n")


if __name__ == "__main__":
    test_init_grid()
    test_check_legal()
    test_legal_moves()
    # test_merge_sort()
    test_pick_move_nn()
    test_pick_rand_move()
