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
    maze.max_time = math.sqrt(maze.size)
    # maze.max_time = 0.01
    time_start = time.time()
    open_heap_start = []
    open_heap_end = []

    open_dictionary_start = {}
    open_dictionary_end = {}

    closed_dictionary_start = {}
    closed_dictionary_end = {}

    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    grid = maze.get_grid()
    second_grid = maze.get_second_grid()

    start_node = grid[x1][y1]
    end_node = second_grid[x2][y2]

    calculate_f_cost(maze, node=start_node, end=end_node)
    heapq.heappush(open_heap_start, start_node)
    open_dictionary_start[start_node] = True

    calculate_f_cost(maze, node=end_node, end=start_node)
    heapq.heappush(open_heap_end, end_node)
    open_dictionary_end[end_node] = True

    current_node_end = end_node

    came_from_start = {}
    came_from_end = {}

    previous_node_start = None
    previous_node_end = None

    while len(open_heap_start) != 0 and len(open_heap_end) and (time.time() - time_start <= maze.max_time):
        current_node_start = heapq.heappop(open_heap_start)
        current_node_start.make_closed()
        open_dictionary_start[current_node_start] = False
        closed_dictionary_start[current_node_start] = True
        draw_node(maze, current_node_start)

        if previous_node_start:
            if not previous_node_start.is_neighbor(current_node_start):
                maze.update_cuttoff(previous_node_start.depth)

        previous_node_start = current_node_start

        temp1 = second_grid[current_node_start.get_x()][current_node_start.get_y()]

        if closed_dictionary_end.get(temp1, False):
            maze.actual_time = time.time() - time_start
            temp1.make_grey()
            draw_node(maze, temp1)
            recreate_bidirectional_path(maze, temp1, came_from_start, came_from_end)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node_start, end_node, open_dictionary_start, closed_dictionary_start, came_from_start, open_heap_start)

        #   second one #######################
        current_node_end = heapq.heappop(open_heap_end)
        current_node_end.make_closed()
        current_node_end.make_blue()
        open_dictionary_end[current_node_end] = False
        closed_dictionary_end[current_node_end] = True
        draw_node(maze, current_node_end)

        if previous_node_end:
            if not previous_node_end.is_neighbor(current_node_end):
                maze.update_cuttoff(previous_node_end.depth)

        previous_node_end = current_node_end

        temp2 = grid[current_node_end.get_x()][current_node_end.get_y()]

        if closed_dictionary_start.get(temp2, False):
            maze.actual_time = time.time() - time_start
            temp2.make_grey()
            draw_node(maze, temp2)
            recreate_bidirectional_path(maze, temp2, came_from_start, came_from_end)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node_end, start_node, open_dictionary_end, closed_dictionary_end, came_from_end, open_heap_end)

    return False


def biAstar_helper(maze, current_node, end_node, open_dictionary, closed_dictionary, came_from, open_heap):
    neighbors = current_node.get_neighbors()
    for neighbor in neighbors:
        if neighbor.get_x() == 10 and neighbor.get_y() == 16:
            print('here')
        neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
        if open_dictionary.get(neighbor, False):
            if neighbor.get_g() <= neighbor_current_cost:
                continue
            closed_dictionary[neighbor] = False
            neighbor.set_g(neighbor_current_cost)
            neighbor.set_depth(current_node.get_depth())
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
            neighbor.set_depth(current_node.get_depth())
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            draw_node(maze, neighbor)
        else:
            neighbor.set_g(neighbor_current_cost)
            neighbor.set_depth(current_node.get_depth())
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            closed_dictionary[neighbor] = False
            draw_node(maze, neighbor)


def recreate_bidirectional_path(maze, node, came_from_start, came_from_end):
    node_x = node.get_x()
    node_y = node.get_y()
    node = maze.get_second_grid()[node_x][node_y]
    maze.get_path().append(node)
    # node.make_path()
    draw_node(maze, node)



    while came_from_end.get(node, False):
        print(123)
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