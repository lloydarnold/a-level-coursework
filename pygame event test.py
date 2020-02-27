import pygame
import threading
import time
from pygame.locals import *


def thread_a():
    while True:
        anEvent = pygame.event.Event(KEYDOWN, message="empty")
        pygame.event.post(anEvent)
        time.sleep(1)


def thread_b():
    while True:
        for event in pygame.event.get():
            print("halleh-fucking-LULAH")


def main():
    pygame.init()
    newThread = threading.Thread(target=thread_a, args=())
    otherThread = threading.Thread(target=thread_b, args=())
    newThread.start()
    otherThread.start()


if __name__ == "__main__":
    main()
