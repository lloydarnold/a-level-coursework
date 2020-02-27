import pygame
import sys
import time
import threading
import os
import neural_network as nn
import random
from pygame.locals import *

# COLOURS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
BAT_SIZE = (5, 40)
BALL_SIZE = (10, 10)

# declare constant octal values for event references
# USEREVENT is pygame local
BAT1UP = USEREVENT + 1
BAT1DOWN = USEREVENT + 2
BAT2UP = USEREVENT + 3
BAT2DOWN = USEREVENT + 4

PROJECT_NAME = "pong"


class Item:
    """
    Defines general item class, for any item that user can interact with
    """
    def __init__(self, xCoord=0, yCoord=0, dimensions=(20, 20), delta_x=0, delta_y=0, colour=WHITE, canvas=""):
        """
        __init__ magic method; class constructor
        :param xCoord: initial x co-ordinate of item
        :param yCoord: initial y co-ordinate of item
        :param dimensions: (x, y) -- dimensions of shape. All shapes in this game are rectangles by default.
        :param delta_x: change in x per move
        :param delta_y: change in y per move
        :param colour: item colour (WHITE by default)
        :param canvas: game surface on which item is to be drawn
        """
        self.x = xCoord
        self.y = yCoord
        self.dimensions = dimensions
        self.colour = colour
        self.movement = [delta_x, delta_y]
        if canvas:
            self.canvas = canvas
        else:
            print("no canvas passed in")

    def wipe(self, x, y):
        tempRect = (x, y, self.dimensions[0], self.dimensions[1])
        pygame.draw.rect(self.canvas, BLACK, tempRect)
        pygame.display.update(tempRect)

    def draw(self):
        """ draws item to screen and updates screen """
        tempRect = (self.x, self.y, self.dimensions[0], self.dimensions[1])
        pygame.draw.rect(self.canvas, self.colour, tempRect)
        pygame.display.update(tempRect)

    def move(self):
        """ method to move item by measurements in self.movement """
        self.wipe(self.x, self.y)
        self.x += self.movement[0]
        self.y += self.movement[1]
        self.adjust_for_boundaries()
        self.draw()

    def adjust_for_boundaries(self):
        """ method to stop item from moving outside the accepted bounds of the game """
        if self.y < 9:
            self.y = 9
        if self.y > SCREEN_HEIGHT - (9 + self.dimensions[1]):
            self.y = SCREEN_HEIGHT - (9 + self.dimensions[1])


class Ball(Item):
    def bounce(self, changeX, changeY):
        if changeX:
            direction = 0
        elif changeY:
            direction = 1
        else:
            return "must set exactly 1 of changeX, changeY to True"

        self.movement[direction] *= -1
        self.movement[1] += random.randint(-2, 2)
        # self.movement[direction] += random.randint(-8, 8)

        if changeY:
            # this stops the side rails from being overwritten when the ball bounces against them
            draw_background(self.canvas)


class Bat(Item):
    def down(self):
        if self.y != 5:
            self.movement[1] = abs(self.movement[1])
            self.move()

    def up(self):
        if self.y != 365:
            self.movement[1] = -1 * abs(self.movement[1])
            self.move()

    def calc_correct(self, ball):
        """ used in gradient descent to calculate 'correct' bat move
            :param ball : instance of Ball class that bat is trying to hit
        """

        # if statement needed rather than abs value as bat position is never 0
        if ball.x > self.x:
            xDist = ball.x - self.x
        else:
            xDist = self.x - ball.x

        # // is floor division operator
        cycles = xDist // ball.movement[0]

        if cycles < 0:
            return "no move needed"

        yIntercept = ball.y + cycles * ball.movement[1]

        if yIntercept < self.y - 5:
            # print("elevator, goin up")
            # print(str(yIntercept) + "  " + str(self.y))
            return "up"
        if yIntercept > self.y + BAT_SIZE[1] / 2:
            # print("down down down down")
            # print(str(yIntercept) + "  " + str(self.y))
            return "down"
        return "no move needed"


def draw_background(canvas):

    pygame.draw.rect(canvas, WHITE, (15, 5, SCREEN_WIDTH - 30, 4))
    pygame.draw.rect(canvas, WHITE, (15, SCREEN_HEIGHT - 9, SCREEN_WIDTH - 30, 4))

    pygame.display.update()


def init_screen():
    pygame.init()
    gameSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    pygame.mouse.set_visible(0)
    gameSurface.fill(BLACK)
    draw_background(gameSurface)
    return gameSurface


def reset_screen(screen):
    screen.fill(BLACK)
    draw_background(screen)


def end_game():
    """ end game correctly """
    pygame.quit()
    sys.exit()


def check_bounce(ball):
    """ Subroutine to check if ball needs to bounce. Will also call bounce if at either rail
        :param ball : instance of ball class
        :returns 1 (int) if bouncing on bat1, 2 (int) if bouncing on bat2"""
    if ball.y <= 10 or ball.y >= SCREEN_HEIGHT - 20:
        ball.bounce(False, True)
    if ball.x >= SCREEN_WIDTH - 25:
        return 2
    if ball.x <= 15:
        return 1


def check_bounce_bat(ball, bat):
    """ Subroutine to check if ball is touching bat (to check bounce)
        :param ball : instance of ball class
        :param bat : instance of bat class
        """
    if bat.y - 8 <= ball.y <= bat.y + BAT_SIZE[1] - 2:
        ball.bounce(True, False)
        return 1
    return 0


def game_over(ball):
    """ checks to see if game is over
     :param ball : instance of ball class
     :returns True if ball is off either end of screen, False if not
     """
    if ball.x < 10 or ball.x > SCREEN_WIDTH - (10 + BALL_SIZE[1]):
        return True
    else:
        return False

# end of pong functionality code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def comp_move(bat=Bat(), ball=Ball(), control_set=(pygame.event.Event(0o0001, message = "no event passed"),
pygame.event.Event(0o0001, message = "no event passed")), stop=None):
    """
     perfect computer mover thread.
    :param bat: instance of the bat class
    :param ball: instance of the Ball class. Should be ball in game at time
    :param control_set: tuple of 2 pygame events. Index 0 to move bat up, index 1 to move it down
    :param stop: lambda function to stop thread execution
    """

    while True:
        time.sleep(0.02)
        correctMove = bat.calc_correct(ball)
        if correctMove == "up":
            pygame.event.post(control_set[0])
        if correctMove == "down":
            pygame.event.post(control_set[1])

        if stop():
            break


def neural_net_move(network = nn.NeuralNet(), inputArray=None, control_set=(pygame.event.Event(0o0001, message = "no event passed"),
pygame.event.Event(0o0001, message = "no event passed")), stop=None):
    """
    computer mover thread, using neural network to evaluate moves.
    :param network: instance of neural_network.NeuralNet class
    :param inputArray: lambda function that, when called, returns array to be input to neural net
    :param bat: instance of the Bat
    :param ball: instance of Ball class. Should be ball that bat is trying to hit
    :param control_set: tuple of 2 pygame events. Index 0 to move bat up, index 1 to move it down
    :param stop: lambda function to stop thread execution
    """
    if not inputArray:
        print("must pass inputArray into neural_net_move")
        return

    while True:
        time.sleep(0.1)
        arrIn = [inputArray()]
        network.run_first_layer(arrIn)
        # for x in range(0, len(network.layers)-1):
        #   network.feed_forward(x)
        network.feed_forward(1)
        network.feed_forward(2)
        network.feed_forward(3)
        val = network.rtn_rating()
        # set to use hyperbolic tangent function. could use any other logistic sigmoidal
        # function with range -1, 1 inclusive. Values > 0.3 mean move up. Values < 0.3 mean move down
        # value x such that -0.3 < x < 0.3 will result in no move being made
        if val > 0.3:
            pygame.event.post(control_set[0])
        if val < -0.3:
            pygame.event.post(control_set[1])
        if stop():
            break


def fitness_func(canvas, netToTest):
    """ subroutine for game play
    :param canvas : pygame surface on which gameplay occurs
    :param netToTest : instance of network class, fitness of which is being evaluated
    """
    # initialise game objects
    gameBall = Ball(50, 50, BALL_SIZE, 5, 5, WHITE, canvas)
    bat1 = Bat(10, 180, BAT_SIZE, 0, 20, WHITE, canvas)
    bat2 = Bat(SCREEN_WIDTH - 15, 180, BAT_SIZE, 0, 20, WHITE, canvas)

    bat1.draw()
    bat2.draw()
    gameBall.draw()

    # initialise variables for new thread calls
    stop_threads = False
    input_nn = [gameBall.x, gameBall.y, bat1.x, bat1.y, gameBall.movement[0], gameBall.movement[1]]
    bat1_controls = [pygame.event.Event(BAT1UP, message="move bat 1 up"),
                     pygame.event.Event(BAT1DOWN, message="move bat 1 down")]
    bat2_controls = [pygame.event.Event(BAT2UP, message="move bat 2 up"),
                     pygame.event.Event(BAT2DOWN, message="move bat 2 down")]

    # net = nn.NeuralNet((6, 40, 20, 1), 1, False, "pls work bby", 1, PROJECT_NAME)

    # start new threads
    comp_control_thread = threading.Thread(target=comp_move, args=(bat2, gameBall, bat2_controls, lambda: stop_threads,))
    neural_net_thread = threading.Thread(target=neural_net_move, args=(netToTest, lambda: input_nn, bat1_controls, lambda: stop_threads))
    comp_control_thread.start()             # N.B. Thread.start() instead of Thread.run()
    neural_net_thread.start()               # Thread.run() moves main thread, Thread.start() initiates new

    bounces = 0
    play_count = 1000

    while play_count > 0:
        time.sleep(0.01)
        play_count -= 1

        for event in pygame.event.get():
            # processes every event since last cycle - this stops game ignoring one player if multiple keys hit
            # simultaneously. For more on pygame events, see documentation
            if event.type == QUIT:
                end_game()
            else:
                if event.type == BAT1UP:
                    bat1.up()
                if event.type == BAT1DOWN:
                    bat1.down()
                if event.type == BAT2UP:
                    bat2.up()
                if event.type == BAT2DOWN:
                    bat2.down()

        input_nn = [gameBall.x, gameBall.y, bat1.x, bat1.y, gameBall.movement[0], gameBall.movement[1]]
        gameBall.move()  # calls move method on ball

        bounceOnBat = check_bounce(gameBall)
        if bounceOnBat == 1:
            bounces += check_bounce_bat(gameBall, bat1)
        if bounceOnBat == 2:
            check_bounce_bat(gameBall, bat2)

        if gameBall.x < 10:
            gameBall.bounce(True, False)
            gameBall.x += 5

    stop_threads = True
    del gameBall
    del bat1
    del bat2
    return bounces


def train(networks=(), gens=2, startGen=0):
    print("beginning random phase of training.")
    prevGenBottomFitness = 0
    prevGenTopFitness = 0
    canvas = init_screen()

    for h in range(1, gens):

        genTopFitness = -999
        genBottomFitness = 999

        start = time.time()

        numOfNets = len(networks)
        currentNet = 0

        for network in networks:
            network.fitness = fitness_func(canvas, network)
            reset_screen(canvas)
            if network.fitness > genTopFitness:
                genTopFitness = network.fitness

            if network.fitness < genBottomFitness:
                genBottomFitness = network.fitness
            currentNet += 1
            print("%d%% of games in generation %d have been played"
                  % (round((100 * (currentNet / numOfNets)), 1), startGen + h))

        # rank generation
        networks = nn.rank_generation(networks)

        nn.save_generation(networks)
        # save_generation(networks)

        nn.save_meta_data((("top win rate ", genTopFitness), ("bottom win rate ", genBottomFitness)
                           , ("diff top ", genTopFitness - prevGenTopFitness)
                           , ("diff bottom ", genBottomFitness - prevGenBottomFitness))
                          , networks)

        nn.eliminate_bottom_networks(networks)

        nn.mutate_and_update(networks)

        end = time.time()

        prevGenTopFitness = genTopFitness
        prevGenBottomFitness = genBottomFitness

        print("generation %s complete in %d seconds" % (h, end - start))
    return networks


def init_networks(sizeOfGen=4):
    """ initialises array of networks """
    nets = []
    for i in range(0, sizeOfGen):
        nets.append(nn.NeuralNet((6, 40, 20, 1), 1, False, None, 1, PROJECT_NAME))

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
        try:
            directories = [f.path for f in os.scandir(path) if f.is_dir()]
        except FileNotFoundError:
            print("error, file path specified does not exist. gen number entered was %d" %genReached)
            return
        netsFound = []

        for x in directories:
            # print(x[-13:])
            network = nn.NeuralNet((6, 40, 20, 1), 1, True, x[-13:], genReached, PROJECT_NAME)
            netsFound.append(network)

        return netsFound, genReached
    return


def main():
    canvas = init_screen()
    # play_game(canvas)

    numOfGens = get_value("How many generations? ")

    if ask_load():
        networks, startGen = load()
    else:
        numOfNets = int(get_value("Generation size? "))
        networks = init_networks(numOfNets)
        startGen = 0

    train(networks, int(numOfGens), int(startGen))

    print("and that's the game folks")


if __name__ == "__main__":
    main()
