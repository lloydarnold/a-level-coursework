import pygame
import random
import sys
import time
from pygame.locals import *

# COLOURS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
BAT_SIZE = (5, 40)
BALL_SIZE = (10, 10)


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
        self.wipe(self.x, self.y)
        self.x += self.movement[0]
        self.y += self.movement[1]
        self.adjust_for_boundaries()
        self.draw()

    def adjust_for_boundaries(self):
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
        # self.movement[direction] += random.randint(-8, 8)
        for direc in self.movement:
            if abs(direc) < 4:
                direc = int(1.5 * direc)
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
            :param ball : instance of ball class
        """
        return 1


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


def game_over(ball):
    """ checks to see if game is over
     :param ball : instance of ball class
     :returns True if ball is off either end of screen, False if not
     """
    if ball.x < 10 or ball.x > SCREEN_WIDTH - (10 + BALL_SIZE[1]):
        return True
    else:
        return False


if __name__ == "__main__":
    canvas = init_screen()

    # pygame.draw.circle(canvas, WHITE, (100, 100), 26)
    # pygame.display.update()

    # object1 = Item(100, 100, (20,20), 10, 10, WHITE, canvas)
    # object1.draw()

    gameBall = Ball(50, 50, BALL_SIZE, 5, 5, WHITE, canvas)
    bat1 = Bat(10, 180, BAT_SIZE, 0, 20, WHITE, canvas)
    bat2 = Bat(SCREEN_WIDTH - 15, 180, BAT_SIZE, 0, 20, WHITE, canvas)

    bat1.draw()
    bat2.draw()
    gameBall.draw()

    gamePlaying = True

    while gamePlaying:
        time.sleep(0.05)

        for event in pygame.event.get():
            # processes every event since last cycle - this stops game ignoring one player if multiple keys hit
            # simultaneously. For more on pygame events, see documentation
            if event.type == QUIT:
                end_game()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    bat1.up()
                if event.key == K_DOWN:
                    bat1.down()

                if event.key == K_w:
                    bat2.up()
                if event.key == K_s:
                    bat2.down()

        gameBall.move()  # calls move method on ball

        bounceOnBat = check_bounce(gameBall)
        if bounceOnBat == 1:
            check_bounce_bat(gameBall, bat1)
        if bounceOnBat == 2:
            check_bounce_bat(gameBall, bat2)

        if game_over(gameBall):
            gamePlaying = False

    print("and that's the game folks")
