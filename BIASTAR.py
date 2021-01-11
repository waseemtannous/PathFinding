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

def biAstar(maze):

    time_start = time.time()
    open_heap_start = []
    open_heap_end = []

    open_dictionary_start = {}
    open_dictionary_end = {}

    closed_dictionary_start = {}
    closed_dictionary_end = {}

    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    calculate_f_cost(maze, node=start_node, end=end_node)
    heapq.heappush(open_heap_start, start_node)
    open_dictionary_start[start_node] = True

    calculate_f_cost(maze, node=end_node, end=start_node)
    heapq.heappush(open_heap_end, end_node)
    open_dictionary_end[end_node] = True

    current_node2 = end_node

    came_from_start = {}
    came_from_end = {}

    while len(open_heap_start) != 0 and len(open_heap_end) and maze.running:
        current_node = heapq.heappop(open_heap_start)
        if current_node.get_x() == 19 and current_node.get_y() == 16:
            print('here')
        current_node.make_closed()
        open_dictionary_start[current_node] = False
        closed_dictionary_start[current_node] = True
        draw_node(maze, current_node)
        if closed_dictionary_end.get(current_node, False):
            print('found from end')
            maze.found = True
            time_end = time.time()
            current_node.make_grey()
            draw_node(maze, current_node)
            recreate_bidirectional_path(maze, current_node, came_from_start, came_from_end)
            maze.print(time_end - time_start)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node, end_node, open_dictionary_start, closed_dictionary_start, came_from_start, open_heap_start)

        #   second one #######################
        current_node2 = heapq.heappop(open_heap_end)
        if current_node2.get_x() == 19 and current_node2.get_y() == 16:
            print('here')
        current_node2.make_closed()
        current_node2.make_blue()
        open_dictionary_end[current_node2] = False
        closed_dictionary_end[current_node2] = True
        draw_node(maze, current_node2)
        if closed_dictionary_start.get(current_node2, False):
            print('found from start')
            maze.found = True
            time_end = time.time()
            cost = current_node2.get_g()
            current_node2.make_grey()
            draw_node(maze, current_node2)
            recreate_bidirectional_path(maze, current_node2, came_from_start, came_from_end)
            maze.print(time_end - time_start)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node2, start_node, open_dictionary_end, closed_dictionary_end, came_from_end, open_heap_end)

    return False


def biAstar_helper(maze, current_node, end_node, open_dictionary, closed_dictionary, came_from, open_heap):
    neighbors = current_node.get_neighbors()
    for neighbor in neighbors:
        neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
        if open_dictionary.get(neighbor, False):
            if neighbor.get_g() <= neighbor_current_cost:
                continue
            neighbor.set_g(neighbor_current_cost)
            if came_from[current_node] == neighbor:
                continue
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heapify(open_heap)
            neighbor.make_open()
            draw_node(maze, neighbor)
        elif closed_dictionary.get(neighbor, False):
            if neighbor.get_g() <= neighbor_current_cost:
                continue
            closed_dictionary[neighbor] = False
            neighbor.set_g(neighbor_current_cost)
            if came_from[current_node] == neighbor:
                continue
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            draw_node(maze, neighbor)
        else:
            neighbor.set_g(neighbor_current_cost)
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            closed_dictionary[neighbor] = False
            draw_node(maze, neighbor)


def recreate_bidirectional_path(maze, node, came_from_start, came_from_end):
    maze.get_path().append(node)
    # node.make_path()
    draw_node(maze, node)

    node_x = node.get_x()
    node_y = node.get_y()

    while node in came_from_end:
        node = came_from_end[node]
        node.make_path()
        maze.get_path().append(node)
        node.make_path()
        draw_node(maze, node)

    maze.get_path().reverse()
    node = maze.get_grid()[node_x][node_y]
    print("saji")

    while node in came_from_start:
        node = came_from_start[node]
        print(node.get_x(), ", ", node.get_y())
        node.make_path()
        maze.get_path().append(node)
        node.make_path()
        draw_node(maze, node)
    node = maze.get_grid()[node_x][node_y]
    node.make_grey()
    draw_node(maze, node)