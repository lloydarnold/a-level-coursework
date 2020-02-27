## python code for graphical game reversi

import pygame, sys, time, random, copy, os
from pygame.locals import *

import neural_net_v2 as NN

PROJECTNAME = "Othello"

#############################################################################################################################################################
############################# this section of code is intended to provide a graphical interface for the game, using pygame ##################################
#############################################################################################################################################################
pygame.init()

# declare colours for use in game --------------------------------------------------------------------------------------------------------------------------------
SHADOW = (192, 192, 192)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 128)
LIGHTBLUE = (0, 0, 255)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)
PURPLE = (102, 0, 102)
LIGHTPURPLE = (153, 0, 153)
BLACK = (0, 0, 0)
NULL = (145, 101, 1)

gameSurface = pygame.display.set_mode((530, 530))
pygame.display.set_caption("Reversi")
pygame.mouse.set_visible(1)
gameSurface.fill(LIGHTGREEN)


def show_scores(pieces):
    fontObj = pygame.font.SysFont(cambria, 18)
    textsurface = fontObj.render("WHite pieces : " + str(pieces("white:")), True, BLACK, WHITE)

    if location == "centre":
        textRectObject.center = (270, 300)

    gameSurface.blit(textsurface, textRectObject)
    pygame.display.update()


def GUI_draw_grid():
    for x in range(0, 9):
        pygame.draw.rect(gameSurface, GREEN, (16, (16 + 62 * x), 497, 2))
        pygame.draw.rect(gameSurface, GREEN, ((16 + 62 * x), 16, 2, 497))
        pygame.display.update()


class tile():  # every gamepiece is treated as an object. draw draws it to screen, flip changes it's colour, draw_ghost shows a user that that square is playable

    def __init__(self, colour, x, y):
        self.colour = colour
        if self.colour == BLACK:
            self.oppcolour = WHITE
        else:
            self.oppcolour = BLACK
        self.x = 47 + 62 * x;
        self.y = 47 + 62 * y

    def draw(self):
        pygame.draw.circle(gameSurface, self.colour, (self.x, self.y), 26)
        pygame.draw.circle(gameSurface, self.oppcolour, (self.x, self.y), 28, 2)
        pygame.display.update()

    def flip(self):
        temp = self.colour;
        self.colour = self.oppcolour;
        self.oppcolour = temp
        self.draw()

    def show_ghost(self):
        pygame.draw.rect(gameSurface, SHADOW, (self.x - 10, self.y - 10, 20, 20))
        pygame.display.update((self.x - 10, self.y - 10, 20, 20))

    def hide_ghost(self):
        pygame.draw.rect(gameSurface, LIGHTGREEN, (self.x - 10, self.y - 10, 20, 20))
        pygame.display.update((self.x - 10, self.y - 10, 20, 20))


## end of class -------------------------------------------------------------------------------------------------------------------------------------------

# this sub defines an array of tile objects
def define_tiles():
    tiles = [""]
    for i in range(0, 64):
        tiles.append(tile(NULL, i - (8 * (i // 8)), i // 8))
    tiles[28] = tile(WHITE, 3, 3);
    tiles[29] = tile(BLACK, 4, 3);
    tiles[36] = tile(BLACK, 3, 4);
    tiles[37] = tile(WHITE, 4, 4)
    return tiles


# store array of tile objects in mapped array for usability
def define_tileGrid(tiles):
    return [
        # ---        0          1           2          3         4           5          6          7 ----------
        [tiles[1], tiles[2], tiles[3], tiles[4], tiles[5], tiles[6], tiles[7], tiles[8]],  # 0
        [tiles[9], tiles[10], tiles[11], tiles[12], tiles[13], tiles[14], tiles[15], tiles[16]],  # 1
        [tiles[17], tiles[18], tiles[19], tiles[20], tiles[21], tiles[22], tiles[23], tiles[24]],  # 2
        [tiles[25], tiles[26], tiles[27], tiles[28], tiles[29], tiles[30], tiles[31], tiles[32]],  # 3
        [tiles[33], tiles[34], tiles[35], tiles[36], tiles[37], tiles[38], tiles[39], tiles[40]],  # 4
        [tiles[41], tiles[42], tiles[43], tiles[44], tiles[45], tiles[46], tiles[47], tiles[48]],  # 5
        [tiles[49], tiles[50], tiles[51], tiles[52], tiles[53], tiles[54], tiles[55], tiles[56]],  # 6
        [tiles[57], tiles[58], tiles[59], tiles[60], tiles[61], tiles[62], tiles[63], tiles[64]],  # 7
    ]


def reset_board(tiles):
    """ This subroutine resets the tile grid """

    for tileRef in tiles:
        if tileRef != "": pygame.draw.circle(gameSurface, LIGHTGREEN, (tileRef.x, tileRef.y), 29)
    return 0


def init_board():
    """ initialises drawing of board and tileGrid. returns tileGrid"""
    GUI_draw_grid()
    tiles = define_tiles()
    tileGrid = define_tileGrid(tiles)
    reset_board(tiles)
    tiles[28].draw();
    tiles[29].draw();
    tiles[36].draw();
    tiles[37].draw()
    return tileGrid


###########################################################################################################################################################

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
def print_board_colours(board):
    """ print colours of tiles on board. For testing only. """
    print("\n\n")
    for row in board:
        for square in row:
            print(str(square.colour).ljust(17), end='')
        print('\n')


# checks along one line to see if any counters would switch ------------------------------------------------------------------------------------------------
def check_line(delta_x, delta_y, grid, row, column, turn):
    if turn == -1:
        p_colour = WHITE; opp_colour = BLACK
    else:
        p_colour = BLACK; opp_colour = WHITE
    if row + delta_y < 0 or row + delta_y > 7 or column + delta_x < 0 or column + delta_x > 7: return False
    if grid[row + delta_y][column + delta_x].colour != opp_colour:
        return False
    step = 1

    while True:
        step += 1
        x_point = column + step * delta_x;
        y_point = row + step * delta_y

        if x_point < 0 or x_point > 7 or y_point < 0 or y_point > 7 or (delta_x == 0 and delta_y == 0):
            return False
        elif grid[row + step * delta_y][column + step * delta_x].colour == p_colour:
            return [delta_x, delta_y]
        elif grid[row + step * delta_y][column + step * delta_x].colour == NULL:
            return False

    return False


# checks move is legal -----------------------------------------------------------------------------------------------------------------------------------------------
def check_legal(grid, row, column, turn, directions=[]):
    if grid[row][column].colour != NULL: return False
    for x in range(-1, 2):
        for y in range(-1, 2):
            directions.append(check_line(x, y, grid, row, column, turn))
            if directions[-1] == False: directions.pop()
    if directions == []:
        return False
    else:
        return True


# checks there are legal moves remaining -----------------------------------------------------------------------------------------------------------------------------
def moves_remaining(grid, turn):
    for row in range(0, 8):
        for column in range(0, 8):
            if check_legal(grid, row, column, turn, []) == True: return True
    return False


# convert from raw pixel values to x/y references --------------------------------------------------------------------------------------------------------------------
def process_move(rawMove):
    move = [0, 0]
    move[0] = (rawMove[0] - 16) // 62
    move[1] = (rawMove[1] - 16) // 62
    if move[0] > 7 or move[1] > 7: move = [4,
                                           4]  # if the move falls outside the legal bounds then I set it to [4, 4] as this is always an illegal move

    return move


# take the co-ordinates of the user's mouse click and process into grid reference-------------------------------------------------------------------------------------
def user_move_click(grid, turn, directions):
    ghosts = display_ghosts(grid, turn)

    while True:
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            rawMove = pygame.mouse.get_pos()
            move = process_move(rawMove)
            if check_legal(grid, move[1], move[0], turn, directions) == True:
                hide_ghosts(grid, ghosts)
                return [move[1], move[0]]
    return 0


# this subroutine displays the squares in which the user can play -------------------------------------------------------------------------------------------------------
def display_ghosts(board=[], turn=1):
    moves = legal_moves(board, turn);
    ghosts = []
    for move in moves:
        board[move[0][0]][move[0][1]].show_ghost()
        ghosts.append(move[0])
    return ghosts


# who you gonna call ?? this subroutine gets rid of the ghost squares --------------------------------------------------------------------------------------------------
def hide_ghosts(board=[], ghosts=[[0, 0]]):
    for ghost in ghosts:
        board[ghost[0]][ghost[1]].hide_ghost()


# change line --------------------------------------------------------------------------------------------------------------------------------------------------------
def change_line(grid, move, delta_x, delta_y, turn):
    step = 1;
    stop = False
    if turn == -1:
        pColour = WHITE; oppColour = BLACK
    else:
        pColour = BLACK; oppColour = WHITE
    while stop == False:
        if grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == oppColour:
            grid[move[0] + step * delta_y][move[1] + step * delta_x].flip();
            step += 1
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == pColour:
            stop = True
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == NULL:
            stop = True
        else:
            step += 1
            x_point = move[1] + step * delta_x;
            y_point = move[0] + step * delta_y
            if x_point < 0 or x_point > 7 or y_point < 0 or y_point > 7:
                stop = True
    return 0


# make move ----------------------------------------------------------------------------------------------------------------------------------------------------------
def make_move(grid, turn, move, directions):
    if turn == -1:
        grid[move[0]][move[1]].colour = WHITE
    else:
        grid[move[0]][move[1]].colour = BLACK; grid[move[0]][move[1]].oppcolour = WHITE
    grid[move[0]][move[1]].draw()

    for direction in directions:
        change_line(grid, move, direction[0], direction[1], turn)
    return 0


# where there's a virtual make move there's gotta be a virtual change line.... :) ------------------------------------------------------------------------------------
def virtual_change_line(grid, move, delta_x, delta_y, turn):
    step = 1;
    stop = False
    if turn == -1:
        pColour = WHITE; oppColour = BLACK
    else:
        pColour = BLACK; oppColour = WHITE
    while stop == False:
        if grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == oppColour:
            grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == pColour;
            step += 1
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == pColour:
            stop = True
        elif grid[move[0] + step * delta_y][move[1] + step * delta_x].colour == NULL:
            stop = True
        else:
            step += 1
            x_point = move[1] + step * delta_x;
            y_point = move[0] + step * delta_y
            if x_point < 0 or x_point > 7 or y_point < 0 or y_point > 7:
                stop = True
    return 0


# this function makes changes to the virtual board, but not to the user's display -------------------------------------------------------------------------------------
def make_virtual_move(grid, turn, move, directions):
    if turn == -1:
        grid[move[0]][move[1]].colour = WHITE
    else:
        grid[move[0]][move[1]].colour = BLACK; grid[move[0]][move[1]].oppcolour = WHITE

    for direction in directions:
        virtual_change_line(grid, move, direction[0], direction[1], turn)
    return 0


# count pieces --------------------------------------------------------------------------------------------------------------------------------------------------------
def count_pieces(grid, totalPieces):
    wCount = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if grid[x][y].colour == WHITE: wCount += 1
    bCount = totalPieces - wCount
    return {"Black Pieces": bCount,
            "White Pieces": wCount}


# returns an array of the legal moves availabke
def legal_moves(board, turn):
    moves = []
    for y in range(0, 8):
        for x in range(0, 8):
            directions = []
            if check_legal(board, y, x, turn, directions) == True:
                moves.append([[y, x], directions, 0])

    return moves  # structure moves : [[move, directions, rating], [move, directions, rating], etc]


# rates moves based on immediate piece gains with corner / edge bias
def rate_board(totalPieces=0, whiteCount=0, board=[], directions=[], turn=1):  # this is a simple evaluation function
    pieces = count_pieces(board, totalPieces)
    newWhiteCount = pieces["White Pieces"]
    lostWhite = whiteCount - newWhiteCount

    if turn == -1:
        pColour = WHITE; oppColour = BLACK
    else:
        pColour = BLACK; oppColour = WHITE

    if turn == 1:
        rating = lostWhite
    else:
        rating = - lostWhite

    edgeBonus = 7
    for row in board:
        if row[0].colour == pColour or row[7].colour == pColour: rating += edgeBonus
        if row[0].colour == oppColour or row[7].colour == oppColour: rating -= edgeBonus

    for square in board[0]:
        if square.colour == pColour: rating += edgeBonus
        if square.colour == oppColour: rating -= edgeBonus

    for square in board[7]:
        if square.colour == pColour: rating += edgeBonus
        if square.colour == oppColour: rating -= edgeBonus

    return rating


def pick_random_move(legalMoves):
    """ randomly picks move from array of legal moves"""
    return legalMoves[random.randint(0, len(legalMoves) - 1)]


def prep_board(board, pColour, oppColour):
    """ This function converts the board to an array of 1s, 0s and -1s, so that the neural net can process it
    Takes input of board as two dimensional array (list of lists), pColour and oppColour as one of the constants declared at top of code"""
    outputBoard = []
    for row in board:
        tempRow = []
        for square in row:
            if square.colour == pColour:
                tempRow.append(1)
            if square.colour == oppColour:
                tempRow.append(-1)
            elif square.colour == NULL:
                tempRow.append(0)
        outputBoard.append(tempRow)
    return outputBoard


def eval_move_with_neural_net(modelBoard=[[]], moves=[], turn=1,
                              network=NN.neural_net([64, 42, 1], [[[[1]] * 64], [[[-999]] * 42], [[[-999]] * 1]],
                                                    "network_one")):
    """ Evaluates a move using neural network and returns the 'best', according to the network
        Takes input of board (as nested list of tile objects, moves (nested list, consisting of move, direction vectors and blank value of rating) and turn as integer = 1 or = -1)"""
    # network = NN.neural_net([64, 42, 1], [ [ [[1]] * 64 ], [ [[-999]] * 42 ], [ [[-999]] * 1 ] ], "network_one")

    # network.save_network()
    # weights = NN.read_weights_from_file("network_one.txt")

    if turn == 1:
        pColour = BLACK; oppColour = WHITE
    elif turn == -1:
        pColour = WHITE; oppColour = BLACK
    else:
        print("passed an invalid val of turn into eval_move_with_neural_net"); pColour = WHITE; oppColour = BLACK

    bestMove = [[4, 4]];
    bestVal = -999

    for move in moves:
        clonedBoard = copy.deepcopy(modelBoard)
        make_virtual_move(clonedBoard, turn, move[0], move[1])

        network.run_first_layer(prep_board(clonedBoard, pColour, oppColour))
        network.feed_forward(1)
        network.feed_forward(2)
        val = network.rtn_rating()

        if val > bestVal:
            bestMove = move;
            bestVal = val
        if val == bestVal:  # unlikely for moves to receive same rating but if they do then code randomly chooses one of them
            if random.randint(0, 1) == 1: bestMove = move

    return bestMove


# this function runs the computer move algorithm and returns moveInfo
def computer_move(board, turn, playerType, neuralNet=-999):
    """ Gets computer move.
    board as list of lists (2d array), turn as integer = 1 or = -1, playerType as integer
    type 1 refers to NN, 2 to random mover, 3 to slightly bias greedy mover, 4 to minimax
    if playerType = 1 and a specific NN is desired, pass this as a parameter. Else, leave blank.
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


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_move(grid, turn, directions, totalPieces, humanTurn):
    """ Provides interface between game and player, meaning that game will treat human and computer players the same
    As of 13:48 22/05/19 requires :
                                    grid as 2d list, turn as integer = -1 or = 1, directions as empty list, totalPieces as integer,
                                    humanTurn as boolean to tell computer how to handle move
                                    """
    moveInfo = ["", ""]
    if humanTurn == True:
        moveInfo[0] = user_move_click(grid, turn, directions)
        moveInfo[1] = directions

    if humanTurn == False:
        moveInfo = computer_move(grid, turn, 1)

    return moveInfo


def init_networks(sizeOfGen=4):
    """ initialises array of networks """
    networks = []
    for i in range(0, sizeOfGen):
        networks.append(
            NN.neural_net([64, 42, 1], [[[[1]] * 64], [[[-999]] * 42], [[[-999]] * 1]], "network_{}".format(i), 1))
    return networks


def play_random_mover(network, numOfGames):
    network.score = 0
    for i in range(0, numOfGames):
        comp_play(network, "n/a", True)

    return (network.score / (numOfGames * 3)) * 100


def training(generations):
    networks = init_networks(6)

    for h in range(1, generations + 1):

        for i in range(0, len(networks)):
            for j in range(0, len(networks)):
                if i != j:
                    comp_play(networks[i], networks[j], False)

        # rank generation
        ##### code up mergesort #####
        networks = rank_generation(networks)

        # save generation
        save_generation(networks)

        # play winner against random mover
        # winRate is percentage
        topWinRate = play_random_mover(networks[0], 100)
        tenWinRate = play_random_mover(networks[3], 100)

        # store win data
        # store_metadata(topWinRate, tenWinRate, networks)     ################ this one hasn't actually been written yet

        # eliminate bottom networks
        eliminate_bottom_networks(networks)

        # mutate & update
        mutate_and_update(networks)

    return 0


def mutate_and_update(networks):
    i = 0
    for network in networks:
        network.mutate_network();
        network.score = 0;
        network.generation += 1;
        network.name = "network_{}".format(i);
        i += 1

    return 0


def store_metadata(top, ten, networks):
    fWinRate = open(top.path, 'w')
    ########################### write this thing <<---------
    fWinRate.close()
    return 0


def eliminate_bottom_networks(networks):
    """ removes bottom half of table of networks and replaces them with the corresponding upper ones """

    for i in range(0, int(len(networks) / 2)):
        networks[-(i + 1)] = copy.deepcopy(networks[i])


def save_generation(networks):
    """ saves all networks in generation. takes input of networks list"""
    for network in networks:
        network.make_net_dir(PROJECTNAME);
        network.save_network()


def rank_generation(networks):
    """ sort generations by score from league. currently uses bubble so change this """
    sorted = False;
    n = len(networks) - 1
    while sorted == False and n != 1:
        for x in range(0, n):
            sorted = True
            if networks[x].score > networks[x + 1].score:
                networks[x + 1], networks[x] = networks[x], networks[x + 1]
                sorted = False
        n -= 1
    return networks


def comp_play(player1, player2, randomMover):
    tileGrid = init_board()
    turn = -1
    totalPieces = 4

    playGame = True;
    playMode = 1

    while playGame == True:

        pygame.event.get()
        directions = []

        if turn == -1:
            moveInfo = computer_move(tileGrid, turn, playMode,
                                     player1)  ## used computer_move func, as opposed to get_move, as always will be playing computer in this sub
        elif turn == 1:
            if randomMover == True: playMode = 2
            moveInfo = computer_move(tileGrid, turn, playMode, player2)

        make_move(tileGrid, turn, moveInfo[0], moveInfo[1])

        totalPieces += 1

        pieces = count_pieces(tileGrid, totalPieces)

        turn *= -1

        if moves_remaining(tileGrid, turn) == False: playGame = False

    if pieces["White Pieces"] > pieces["Black Pieces"]:
        print("White wins"); player1.score += 3
    elif pieces["White Pieces"] == pieces["Black Pieces"]:
        print("draw");
        if player2 != 'n/a': player2.score += 3
    else:
        print("Black wins")
        player1.score += 1
        if player2 != 'n/a': player2.score += 1

    return 0


# main--------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    training(20)

    # GUI_draw_grid()
    tileGrid = init_board()

    # tiles = define_tiles()
    # tileGrid = define_tileGrid(tiles)
    turn = -1
    # tiles[28].draw() ; tiles[29].draw() ; tiles[36].draw() ; tiles[37].draw()
    totalPieces = 4

    humanTurn = True
    playGame = True

    while playGame == True:

        pygame.event.get()
        directions = []

        moveInfo = get_move(tileGrid, turn, directions, totalPieces, humanTurn)
        make_move(tileGrid, turn, moveInfo[0], moveInfo[1])
        totalPieces += 1

        pieces = count_pieces(tileGrid, totalPieces)
        print(str(pieces))

        turn *= -1
        if humanTurn == False:
            humanTurn = True
        else:
            humanTurn = False
        if moves_remaining(tileGrid, turn) == False: playGame = False

    if pieces["White Pieces"] > pieces["Black Pieces"]:
        print("White wins")
    elif pieces["White Pieces"] == pieces["Black Pieces"]:
        print("draw")
    else:
        print("Black wins")