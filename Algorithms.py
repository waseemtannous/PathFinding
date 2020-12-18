import pygame
from Colors import *


def draw(maze):
    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Path Finding")

    # make screen
    WIN.fill(WHITE)

    for row in maze.get_grid():
        for node in row:
            pygame.draw.rect(WIN, node.color, (node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(), maze.get_square_size()))

    # draw grid
    for i in range(maze.get_size()):
        pygame.draw.line(WIN, GREY, (0, i * maze.get_square_size()), (WIDTH, i * maze.get_square_size()))
        for j in range(maze.get_size()):
            pygame.draw.line(WIN, GREY, (j * maze.get_square_size(), 0), (j * maze.get_square_size(), WIDTH))
    pygame.display.update()






def astar(maze):
    draw(maze=maze)



def ids(maze):
    draw(maze=maze)


def ucs(maze):
    draw(maze=maze)


def idAstar(maze):
    draw(maze=maze)


def biAstar(maze):
    draw(maze=maze)


def heuristic1():
    return 0


def heuristic2():
    return 0
