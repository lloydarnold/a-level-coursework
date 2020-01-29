# whats POPPIN folks i'm here to present to you a hot and exciting project that trains a Neural Network to play Reversi
# WAHEYYY let's gooooooo
# 1 represents black pieces

# error 22:02 21/01/2020 - neural_network.py; problem with statement weight += 0.05 * ... line 23
# float object not iterable
# weights not of list like form ??
# do an investigate


import neural_network as NN
import time
import random
import copy
import os

PROJECT_NAME = "opti_reversi2"


def initiate_grid():
    """ passes back nested list of board as integers; 8 by 8. """
    return [
       # 0  1  2  3  4  5  6  7 ----------
        [0, 0, 0, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, -1, 1, 0, 0, 0],  # 3
        [0, 0, 0, 1, -1, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 0],  # 5
        [0, 0, 0, 0, 0, 0, 0, 0],  # 6
        [0, 0, 0, 0, 0, 0, 0, 0],  # 7
    ]


def check_line(delta_x, delta_y, grid, row, column, turn):
    """ checks along one line to see if any counters would switch """
    if row + delta_y < 0 or row + delta_y > 7 or column + delta_x < 0 or column + delta_x > 7: return False
    if grid[row + delta_y][column + delta_x] != turn * -1:
        return False
    step = 1

    while True:
        step += 1
        x_point = column + step * delta_x
        y_point = row + step * delta_y
        if x_point < 0 or x_point > 7 or y_point < 0 or y_point > 7 or delta_x == 0 and delta_y == 0:
            return False
        elif grid[row + step * delta_y][column + step * delta_x] == turn:
            return [delta_x, delta_y]
        elif grid[row + step * delta_y][column + step * delta_x] == 0:
            return False


def check_legal(grid, row, column, turn, directions=(0,0)):
    """ checks move is legal """
    row -= 1
    column -= 1
    if grid[row][column] != 0:
        return False
    for x in range(-1, 2):
        for y in range(-1, 2):
            directions.append(check_line(x, y, grid, row, column, turn))
            if not directions[-1]:
                directions.pop()
    if not directions:
        return False
    else:
        return True


def moves_remaining(grid=(initiate_grid()), turn=-1):
    """ checks there are legal moves remaining
    :param grid as 2d list representing board
    :param turn as integer = 1 or = -1 representing turn"""
    for row in range(1, 9):
        for column in range(1, 9):
            if check_legal(grid, row, column, turn):
                return True
    return False


def change_line(grid, move, delta_x, delta_y, turn):
    """ changes line of counters """
    step = 1
    stop = False
    while not stop:
        if grid[move[0] + step * delta_y][move[1] + step * delta_x] == turn * -1:
            grid[move[0] + step * delta_y][move[1] + step * delta_x] = turn
            step += 1
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x] == turn:
            stop = True
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x] == 0:
            stop = True
        else:
            step += 1
            x_point = move[1] + step * delta_x
            y_point = move[0] + step * delta_y
            if x_point < 0 or x_point > 7 or y_point < 0 or y_point > 7:
                stop = True
    return 0


def make_move(grid, turn, move, directions):
    grid[move[0]][move[1]] = turn  # move is [ y , x ] !!!!!!!!!!!!!!!!!!!!!!!!!!! idk why lmao
    for direction in directions:  # directions should be in form [[x, y], [x, y], etc]
        change_line(grid, move, direction[0], direction[1], turn)


def count_pieces(grid):
    """ returns the number of pieces belonging to a particular player. takes grid as 2d array and turn as integer """
    bCount = 0
    wCount = 0
    for row in grid:
        for square in row:
            if square == 1:
                bCount += 1
            elif square == -1:
                wCount += 1

    return {"Black Pieces": bCount,
            "White Pieces": wCount}


def legal_moves(board, turn):
    """ returns an array of the legal moves available """
    moves = []
    for y in range(0, 8):
        for x in range(0, 8):
            directions = []
            if check_legal(board, y + 1, x + 1, turn, directions) == True:
                moves.append([[y, x], directions, 0])

    return moves  # structure moves : [[move, directions, rating], [move, directions, rating], etc]


# can delete if save_meta_data in neural_network works as expected
def store_metadata(topWR, bottomWR, diffTop, diffBott, networks):
    metaPath = networks[0].path.replace(networks[0].name, "meta.txt")
    fMeta = open(metaPath, 'w')

    fMeta.write("{topWR: %d \n bottomWR: %d \n diffTop: %d \n diffBott: %d }s" % (topWR, bottomWR, diffTop, diffBott))
    # fMeta.write(networks)

    fMeta.close()
    return 0


def rank_generation(networks):
    """ sort generations by score from league. currently uses bubble so change this """
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


def mergesort(arr, left=-11, right=-11):
    """
    sorts generations by score
    :param arr: list of items to sort
    :param left: left pointer
    :param right: right pointer
    :return: networks: sorted list
    """
    if right == -11:
        right = len(arr) - 1
    if left == -11:
        left = 0

    if right > left:

        mid = int((left+right) / 2)
        arr1 = mergesort(arr, left, mid)
        arr2 = mergesort(arr, mid + 1, right)
        merge_nets(arr1, arr2)

    return arr


def merge_nets(nets1, nets2):
    """
    Merge array. Half of mergesort.
    :param nets1: list of networks
    :param nets2: list of networks
    :return: merged array
    """

    len1 = len(nets1)
    len2 = len(nets2)
    merged = []                                 # if it ain't broke, don't fix it.
    pointer1 = 0
    pointer2 = 0

    while pointer1 < len1 and pointer2 < len2:
        hold1 = nets1[pointer1].fitness; hold2 = nets2[pointer2].fitness
        merged.append(max(hold1, hold2))
        if hold1 > hold2:
            pointer1+=1
        elif hold1 < hold2:
            pointer2+=1
        elif hold1 == hold2:
            merged.append(hold2)
            pointer1 +=1
            pointer2 += 1

    if pointer1 < len1:
        merged.append(nets1[pointer1:])
    else:
        merged.append(nets2[pointer2:])

    return merged


def save_generation(networks):
    """ saves all networks in generation. takes input of networks list"""
    for network in networks:
        try:
            network.make_net_dir(PROJECT_NAME)
        except "Directory Access Failure":
            print("could not make directory at path %s" % network.path)
        else:
            print("successfully made directory as path %s" % network.path)
            try:
                network.save_network()
            except "Directory Access Failure":
                print("could not write to directory %s" % network.path)

    return 0


def eval_move_with_neural_net(modelBoard=(()), moves=(), turn=1,
                              network=NN.NeuralNet([64, 42, 1], 1, False, "network_one", PROJECT_NAME)):
    """ Evaluates a move using neural network and returns the 'best', according to the network
       Takes input of board (as nested list of tile objects, moves (nested list, consisting of move, direction vectors
        and blank value of rating) and turn as integer = 1 or = -1)
        :param modelBoard: board state to analyse. represented as 8x8 nested lists of integers
        :param moves: list of legal moves available
        :param turn: Either 1 or -1; tells computer which player they are
        :param network: Instance of NeuralNetwork class, to be used to analyse board
        :returns bestMove: [x,y] co-ords of best move available (according to network)
        """

    # network = NN.NeuralNet([64, 42, 1], [ [ [[1]] * 64 ], [ [[-999]] * 42 ], [ [[-999]] * 1 ] ], "network_one")

    # weights = NN.read_weights_from_file("network_one.txt")

    bestMove = [[4, 4]]
    bestVal = -999

    for move in moves:
        clonedBoard = copy.deepcopy(modelBoard)
        make_move(clonedBoard, turn, move[0], move[1])

        network.run_first_layer(clonedBoard)
        network.feed_forward(1)
        network.feed_forward(2)
        val = network.rtn_rating()

        if val > bestVal:
            bestMove = move
            bestVal = val
        if val == bestVal:  # unlikely for moves to receive same rating but if they do then code randomly chooses one
            if random.randint(0, 1) == 1:
                bestMove = move

    return bestMove


def pick_random_move(legalMoves):
    """ randomly picks move from array of legal moves"""
    return legalMoves[random.randint(0, len(legalMoves) - 1)]


def computer_move(board, turn, playerType, neuralNet=-999):
    """ Gets computer move.
    :param board = list of lists (2d array),
    :param turn = integer = 1 or = -1
    :param playerType = integer  type 1 refers to NN, 2 to random mover, 3 to slightly bias greedy mover, 4 to minimax
    :param neuralNet = integer or neural net object, -999 by default.
            if playerType = 1 and a specific NN is desired, pass this as a parameter
    """

    if playerType == 1:
        if neuralNet == -999:
            moveInfo = eval_move_with_neural_net(board, legal_moves(board, turn), turn)
        else:
            moveInfo = eval_move_with_neural_net(board, legal_moves(board, turn), turn, neuralNet)
    elif playerType == 2:
        moveInfo = pick_random_move(legal_moves(board, turn))
    elif playerType == 3:
        return 0
    elif playerType == 4:
        return 0

    return moveInfo


def find_random_win_rate(network, numOfGames):
    """ plays given network against a random mover a given number of times and returns the win rate as a percentage"""
    network.fitness = 0
    for i in range(0, int(numOfGames / 2)):
        comp_play("n/a", network, True, True)
        comp_play(network, "n/a", True, False)

    return (network.fitness / (numOfGames * 3)) * 100


def comp_play(player1="n/a", player2="n/a", randomMover=True, randMoveW=False):
    board = initiate_grid()
    turn = -1
    totalPieces = 4

    playGame = True
    playMode = 1

    while playGame:

        if turn == -1:
            if randomMover and randMoveW:
                playMode = 2
            else:
                playMode = 1
            moveInfo = computer_move(board, turn, playMode, player1)
        elif turn == 1:
            if randomMover:
                playMode = 2
            moveInfo = computer_move(board, turn, playMode, player2)

        make_move(board, turn, moveInfo[0], moveInfo[1])

        totalPieces += 1

        pieces = count_pieces(board)

        turn *= -1

        if not legal_moves(board, turn):
            playGame = False

    if pieces["White Pieces"] > pieces["Black Pieces"] and player1 != "n/a":
        player1.fitness += 3
    elif pieces["White Pieces"] == pieces["Black Pieces"] and player2 != "n/a":
        player2.fitness += 3
    else:
        if player1 != "n/a":
            player1.fitness += 1
        if player2 != 'n/a':
            player2.fitness += 1

    return 0


def rand_train_thread(networksSubset):  ############## can work here

    genTopWinRate = -999
    genBottomWinRate = 999

    numOfNets = len(networks)
    currentNet = 0

    for network in networks:
        netWR = find_random_win_rate(network, 16)
        if netWR > genTopWinRate: genTopWinRate = netWR

        if netWR < genBottomWinRate: genBottomWinRate = netWR
        currentNet += 1
        print("%d%% of games in generation %d have been played" % (round(((100 * (currentNet / numOfNets))), 1), 0))


def training_rand_stage(gens, networks, startGen):
    print("beginning random phase of training.")
    prevGenBottomWinRate = 50
    prevGenTopWinRate = 50

    for h in range(1, gens + 1):

        genTopWinRate = -999
        genBottomWinRate = 999

        start = time.time()

        numOfNets = len(networks)
        currentNet = 0

        for network in networks:
            netWR = find_random_win_rate(network, 16)
            if netWR > genTopWinRate:
                genTopWinRate = netWR

            if netWR < genBottomWinRate:
                genBottomWinRate = netWR
            currentNet += 1
            print("%d%% of games in generation %d have been played" % (round((100 * (currentNet / numOfNets)), 1), h))

        # rank generation
        # when update from old_neural_network.py to neural_network.py, change this to NN.rank_generation(networks)
        networks = NN.rank_generation(networks)

        NN.save_generation(networks)
        # save_generation(networks)

        NN.save_meta_data((("top win rate ", genTopWinRate),("bottom win rate ", genBottomWinRate)
                 ,("diff top ", genTopWinRate - prevGenTopWinRate)
                 ,("diff bottom ", genBottomWinRate - prevGenBottomWinRate))
                 , networks)

        NN.eliminate_bottom_networks(networks)

        NN.mutate_and_update(networks)

        end = time.time()

        prevGenTopWinRate = genTopWinRate
        prevGenBottomWinRate = genBottomWinRate

        print("generation %s complete in %d seconds" % (h, end - start))
    return networks


def training_tourn_stage(gens, networks, startGen):
    # for h in range(1, gens + 1):
    #     for i in range(0, len(networks)):
    #         for j in range(0, len(networks)):
    #             if i != j:
    #                 comp_play(networks[i], networks[j], True)

    prevGenTopWinRate = 50
    prevGenBottomWinRate = 50

    print("beginning tournament phase of training.")

    start = time.time()

    numOfNets = len(networks)
    currentNet = 0
    for h in range(1, gens + 1):
        for i in range(0, len(networks)):
            for j in range(0, len(networks)):
                if i != j:
                    comp_play(networks[i], networks[j], True)
            currentNet += 1
            print("%d%% of games in generation %d have been played" % (round((100 * (currentNet / numOfNets)), 1), startGen + h))

        networks = NN.rank_generation(networks)

        NN.save_generation(networks)

        genTopWinRate = find_random_win_rate(networks[0], 30)
        genBottomWinRate = find_random_win_rate(networks[-1], 30)

        NN.save_meta_data((("top win rate ", genTopWinRate), ("bottom win rate ", genBottomWinRate)
                 ,("diff top ", genTopWinRate - prevGenTopWinRate)
                 ,("diff bottom ", genBottomWinRate - prevGenBottomWinRate))
                 , networks)

        NN.eliminate_bottom_networks(networks)

        NN.mutate_and_update(networks)

        end = time.time()

        prevGenTopWinRate = genTopWinRate
        prevGenBottomWinRate = genBottomWinRate

        print("generation %s complete in %d seconds" % (startGen+h, end - start))
        print("gen top win rate = %d" % genTopWinRate)


def init_networks(sizeOfGen=4):
    """ initialises array of networks """
    nets = []
    for i in range(0, sizeOfGen):
        nets.append(NN.NeuralNet([64, 42, 1], 1, False, None, 1, PROJECT_NAME))

    return nets


def get_value(question):
    while True:
        userInput = input(question + "  ")
        confirm = input("You have entered %s, is this correct? (Y/N)" % str(userInput))
        if confirm.upper() == "Y":
            return userInput


def ask_load():
    """
    asks user if they wish to load data from an existing set
    :returns 0 if input == "N", 1 if input == "y"
    """
    while True:
        userInput = input("Would you like to load data from an existing data set? (Y/N)  ").upper()
        if userInput == "N":
            return 0
        if userInput == "Y":
            return 1
        print("Invalid input.")


def load():
    # projectName = get_value("")
    genReached = get_value("Please enter the generation number reached (if unknown, please enter -1)")
    if genReached != -1:
        path = os.path.join(os.getcwd(), PROJECT_NAME, "gen_" + str(genReached))
        directories = [f.path for f in os.scandir(path) if f.is_dir()]
        netsFound = []

        for x in directories:
            # print(x[-13:])
            network = NN.NeuralNet([64, 42, 1], 1, True, x[-13:], genReached, PROJECT_NAME)
            netsFound.append(network)

        return netsFound, genReached
    return 0


if __name__ == "__main__":
    numOfRandGens = int(get_value("How many random generations? "))
    numOfTournGens = int(get_value("How many tournament generations? "))
    # numOfRandGens = 4
    # numOfTournGens = 4

    if ask_load():
        networks, startGen = load()
    else:
        numOfNets = int(get_value("Generation size? "))
        networks = init_networks(numOfNets)
        startGen = 0

# check that startGen is taking correct value
    training_tourn_stage(numOfTournGens, training_rand_stage(numOfRandGens, networks, startGen),
                         startGen+numOfTournGens)
