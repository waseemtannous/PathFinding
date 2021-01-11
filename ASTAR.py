import pygame
import time
import heapq

from Colors import *
from Heuristics import *

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


def astar(maze):
    time_start = time.time()
    open_heap = []

    open_dictionary = {}
    closed_dictionary = {}

    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    calculate_f_cost(maze, node=start_node, end=end_node)
    heapq.heappush(open_heap, start_node)
    open_dictionary[start_node] = True

    while len(open_heap) != 0 and maze.running:
        current_node = heapq.heappop(open_heap)
        current_node.make_closed()
        open_dictionary[current_node] = False
        closed_dictionary[current_node] = True
        draw_node(maze, current_node)

        if current_node.get_parent() is not None:   # tree
            current_node.get_parent().tree_neighbors.append(current_node)

        if current_node.get_x() == end_node.get_x() and current_node.get_y() == end_node.get_y():
            maze.found = True
            time_end = time.time()
            while current_node.get_parent() is not None:
                maze.get_path().append(current_node)
                current_node.make_path()
                draw_node(maze, current_node)
                current_node = current_node.get_parent()
            maze.get_path().append(start_node)
            maze.print(time_end - time_start)
            return True
        maze.update_expanded_nodes()
        neighbors = current_node.get_neighbors()
        for neighbor in neighbors:
            neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
            if open_dictionary.get(neighbor, False):
                if neighbor.get_g() <= neighbor_current_cost:
                    continue
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heapify(open_heap)
                neighbor.make_open()
                draw_node(maze, neighbor)
            elif closed_dictionary.get(neighbor, False):
                if neighbor.get_g() <= neighbor_current_cost:
                    continue
                closed_dictionary[neighbor] = False
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                neighbor.make_open()
                open_dictionary[neighbor] = True
                draw_node(maze, neighbor)
            else:
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                neighbor.make_open()
                open_dictionary[neighbor] = True
                draw_node(maze, neighbor)

    return False
