import reversi_gui_neuro_evolution as grev
import pygame

def create_screen():
    gameSurface = pygame.display.set_mode((530, 530))
    pygame.display.set_caption("Reversi")
    pygame.mouse.set_visible(1)
    gameSurface.fill((0, 255, 0))
    return gameSurface


def test_init_board():
    print("testing init board subroutine from graphical reversi")
    grev.init_board(create_screen())
    print("\n")


if __name__ == "__main":
    test_init_board()
