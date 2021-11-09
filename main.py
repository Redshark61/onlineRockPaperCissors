import pygame
from client import menuScreeen
import variables


def main():

    while True:
        menuScreeen(win)


if __name__ == "__main__":

    pygame.font.init()
    variables.width = 700
    variables.height = 700

    win = pygame.display.set_mode((variables.width, variables.height))
    pygame.display.set_caption("Client")
    main()
