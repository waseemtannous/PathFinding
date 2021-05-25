import math

import pygame
import time
from Colors import *

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))


def draw(maze):
    pygame.display.set_caption("Path Finding")

    # make background white
    WINDOW.fill(WHITE)

    # draw the squares
    for row in maze.get_grid():
        for node in row:
            pygame.draw.rect(WINDOW, node.color, (
                node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
                maze.get_square_size()))

    draw_grid(maze=maze)

    # display on the screen
    pygame.display.update()


def draw_grid(maze):
    for i in range(maze.get_size()):
        pygame.draw.line(WINDOW, GREY, (0, i * maze.get_square_size()), (WIDTH, i * maze.get_square_size()))
        for j in range(maze.get_size()):
            pygame.draw.line(WINDOW, GREY, (j * maze.get_square_size(), 0), (j * maze.get_square_size(), WIDTH))


def draw_node(maze, node):
    pygame.draw.rect(WINDOW, node.color, (
        node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(),
        maze.get_square_size(),
        maze.get_square_size()))
    draw_grid(maze=maze)
    pygame.display.update()


def ids(maze):
    # set maximum run time
    maze.max_time = 5 * math.sqrt(maze.size)
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    # get start and end nodes
    start = grid[x1][y1]
    end = grid[x2][y2]
    max_depth = maze.size * maze.size
    time_start = time.time()
    # depth limit search till max depth
    for depth in range(max_depth):
        # check if time has ended
        if not (time.time() - time_start <= maze.max_time):
            return False
        visited = {start: True}
        if dls(current_node=start, end=end, max_depth=depth, maze=maze, visited=visited, time_start=time_start):
            maze.actual_time = time.time() - time_start
            maze.get_path().append(start)
            return True
        for row in grid:
            for node in row:
                if node.get_cost() == 0:
                    node.make_barrier()
                elif node == start:
                    node.make_start()
                elif node == end:
                    node.make_end()
                else:
                    node.reset()
                pygame.draw.rect(WINDOW, node.color, (
                    node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(),
                    maze.get_square_size(),
                    maze.get_square_size()))
        start.make_start()
        end.make_end()
        draw_grid(maze=maze)
        pygame.display.update()
    return False


# depth limited search
def dls(current_node, end, max_depth, maze, visited, time_start):
    # check if time has ended
    if not (time.time() - time_start <= maze.max_time):
        return False

    # check if current node is the end node
    if current_node == end:
        maze.update_cuttoff(current_node.depth)
        return True

    # if reached the maximum depth, stop recursing.
    if max_depth <= 0:
        maze.update_cuttoff(current_node.depth)
        return False

    # change node color
    neighbors = current_node.get_neighbors()
    for node in neighbors:
        current_cost = current_node.get_g() + node.get_cost()
        if visited.get(node, False):
            if node.get_g() <= current_cost:
                continue
        node.make_open()
        draw_node(maze, node)

    maze.update_expanded_nodes()

    # recurse for all the neighbors
    for node in neighbors:
        current_cost = current_node.get_g() + node.get_cost()
        # check if we have reached this node in less g cost
        if visited.get(node, False):
            if node.get_g() <= current_cost:
                continue

        node.set_depth(current_node.get_depth())
        node.set_parent(current_node)
        visited[node] = True
        node.set_g(current_cost)
        node.make_closed()
        draw_node(maze, node)
        if dls(node, end, max_depth - 1, maze, visited, time_start):
            maze.get_path().append(node)
            node.make_path()
            draw_node(maze, node)
            return True
    maze.update_cuttoff(current_node.depth)
    return False
