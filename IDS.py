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


# depth limited search
def dls(current_node, end, max_depth, maze, visited, time_start):
    if not (time.time() - time_start <= maze.max_time):
        return False

    if current_node == end:
        return True

    # If reached the maximum depth, stop recursing.
    if max_depth <= 0:
        maze.update_cuttoff(current_node.depth)
        return False

    # change node color
    for node in current_node.get_neighbors():
        current_cost = current_node.get_g() + node.get_cost()
        if visited.get(node, False):
            if node.get_g() <= current_cost:
                continue
        node.make_open()
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()

    maze.update_expanded_nodes()
    # Recur for all the vertices adjacent to this vertex
    neighbors = current_node.get_neighbors()
    for node in neighbors:
        current_cost = current_node.get_g() + node.get_cost()
        if visited.get(node, False):
            if node.get_g() <= current_cost:
                continue

        node.set_depth(current_node.get_depth())
        if (node.get_x(), node.get_y()) != maze.get_start():
            node.make_closed()
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()

        node.set_parent(current_node)
        visited[node] = True
        node.set_g(current_cost)
        if dls(node, end, max_depth - 1, maze, visited, time_start):
            node.make_path()
            draw_node(maze, node)
            maze.get_path().append(node)
            return True
    maze.update_cuttoff(current_node.depth)
    return False



def ids(maze):
    maze.max_time = math.sqrt(maze.size)
    # maze.max_time = maze.size
    # maze.max_time = 10000
    # maze.max_time = 0.8
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    start = grid[x1][y1]
    end = grid[x2][y2]
    # depth limit search till max depth
    size = maze.size
    max_depth = size * size # todo: check if ok
    time_start = time.time()
    for depth in range(max_depth):
        if not (time.time() - time_start <= maze.max_time):
            return False
        visited = {start: 0}
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
