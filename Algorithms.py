from queue import PriorityQueue

import pygame
import time
import heapq

from Colors import *

PATH = []
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

to_visit = []
expanded_nodes = []
visited_nodes = []


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


def recreate_path(maze):
    for node in PATH:
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()


def calculate_f_cost(node, end):
    heuristic = heuristic1(node=node, end=end)
    node.set_h(heuristic)
    node.calculate_f()


def astar(maze):
    time_start = time.time()
    open_heap = []

    num_of_nodes = 0

    open_dictionary = {}
    closed_dictionary = {}

    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    calculate_f_cost(node=start_node, end=end_node)
    heapq.heappush(open_heap, start_node)
    open_dictionary[start_node] = True
    num_of_nodes += 1

    while len(open_heap) != 0:
        current_node = heapq.heappop(open_heap)
        current_node.make_closed()
        open_dictionary[current_node] = False
        closed_dictionary[current_node] = True
        draw_node(maze, current_node)
        if current_node.get_x() == end_node.get_x() and current_node.get_y() == end_node.get_y():
            cost = current_node.get_g()
            while current_node.get_parent() != None:
                PATH.append(current_node)
                current_node.make_path()
                draw_node(maze, current_node)
                current_node = current_node.get_parent()
                time_end = time.time()
                print("time in sec: ", time_end - time_start)
            print("cost = ", cost)
            print("num of nodes: ", num_of_nodes)
            return True
        for neighbor in current_node.get_neighbors():
            neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
            if open_dictionary.get(neighbor, False):
                if neighbor.get_g() <= neighbor_current_cost: continue
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(neighbor, end_node)
                heapq.heapify(open_heap)
                neighbor.make_open()
                num_of_nodes += 1
                draw_node(maze, neighbor)
            elif closed_dictionary.get(neighbor, False):
                if neighbor.get_g() <= neighbor_current_cost: continue
                closed_dictionary[neighbor] = False
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(neighbor, end_node)
                heapq.heapify(open_heap)
                neighbor.make_open()
                open_dictionary[neighbor] = True
                num_of_nodes += 1
                draw_node(maze, neighbor)
            else:
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                neighbor.make_open()
                open_dictionary[neighbor] = True
                num_of_nodes += 1
                draw_node(maze, neighbor)

    return False


# depth limited search
def dls(start, end, max_depth, maze, visited, steps):
    if start == end: return True

    # If reached the maximum depth, stop recursing.
    if max_depth <= 0: return False

    # change node color
    # for node in start.get_neighbors():
    #     if node in visited:
    #         if visited.get(node) <= steps:
    #             continue
    #     node.make_open()
    #     pygame.draw.rect(WINDOW, node.color, (
    #         node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
    #         maze.get_square_size()))
    #     draw_grid(maze=maze)
    #     pygame.display.update()

    # Recur for all the vertices adjacent to this vertex
    for node in start.get_neighbors():
        if node in visited:
            if visited.get(node) <= steps:
                continue
        # if (node.get_x(), node.get_y()) != maze.get_start():
        #     node.make_closed()
        # pygame.draw.rect(WINDOW, node.color, (
        #     node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
        #     maze.get_square_size()))
        # draw_grid(maze=maze)
        # pygame.display.update()
        visited[node] = steps
        if dls(node, end, max_depth - 1, maze, visited, steps + 1):
            # node.make_path()
            # PATH.append(node)
            return True
    return False


def ids(maze):
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    start = grid[x1][y1]
    end = grid[x2][y2]
    # depth limit search till max depth
    max_depth = 100  # todo change this
    time_start = time.time()
    for depth in range(max_depth):
        # print("iter ", depth)
        visited = {start: 0}
        if dls(start=start, end=end, max_depth=depth, maze=maze, visited=visited, steps=0):
            # recreate_path(maze)
            time_end = time.time()
            print("time in sec: ", time_end - time_start)
            # cost = 0
            # for node in PATH:
            #     cost += node.get_cost()
            #     print(node.get_x(), ", ", node.get_y())
            # print(cost)
            return True
        # for row in grid:
        #     for node in row:
        #         if node.get_cost() == 0:
        #             node.make_barrier()
        #         elif node == start:
        #             node.make_start()
        #         elif node == end:
        #             node.make_end()
        #         else:
        #             node.reset()
        #         pygame.draw.rect(WINDOW, node.color, (
        #             node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(),
        #             maze.get_square_size(),
        #             maze.get_square_size()))
        # start.make_start()
        # end.make_end()
        # draw_grid(maze=maze)
        # pygame.display.update()
    time_end = time.time()
    print("time in sec: ", time_end - time_start)
    return False


def ucs(maze):
    frontier = PriorityQueue()  # Min heap so we choose the cheapest edge
    visited = set([])  # Keeps the visited nodes and prevent duplicates
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    start_node = grid[x1][y1]
    goal_node = grid[x2][y2]

    if start_node == goal_node:
        return True

    path_cost = 0
    frontier._put((path_cost, start_node))

    while True:
        if frontier._qsize() == 0:  # If we get empty heap that means we cant expand more nodes and gal is not found
            return False

        current_node = frontier._get()
        current_node[1].make_closed()
        pygame.draw.rect(WINDOW, current_node[1].color, (
            current_node[1].get_y() * maze.get_square_size(), current_node[1].get_x() * maze.get_square_size(),
            maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()
        visited.add(current_node)
        path_cost = current_node[0]

        if current_node == goal_node:
            return True
        else:
            neighbors = current_node[1].get_neighbors()
            for node in neighbors:
                frontier._put(((node.get_cost() + path_cost), node))
                node.make_open()
                pygame.draw.rect(WINDOW, node.color, (
                    node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(),
                    maze.get_square_size(),
                    maze.get_square_size()))
                draw_grid(maze=maze)
                pygame.display.update()


def idAstar(maze):
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    threshold = heuristic1(start_node, end_node)
    g = 0

    while True:
        print(123)
        cost_dictionary = {}
        temp = idastar_helper(maze, start_node, end_node, g, threshold, cost_dictionary)
        if temp < 0:
            return True
        elif temp == float("inf"):
            return False
        else:
            threshold = temp


def idastar_helper(maze, node, end_node, g, threshold, visited):
    calculate_f_cost(node, end_node)
    f = node.get_f()

    visited[node] = True

    if node.get_x() == end_node.get_x() and node.get_y() == end_node.get_y():
        return (-1) * f  # returns negative if found

    if f > threshold:
        return f

    minimum = float("inf")

    for neighbor in node.get_neighbors():
        current_g_cost = g + neighbor.get_cost()
        if visited.get(neighbor, False):
            if current_g_cost < neighbor.get_g():
                neighbor.set_g(current_g_cost)
            else:
                continue
        temp = idastar_helper(maze, neighbor, end_node, current_g_cost, threshold, visited)
        if temp < 0:
            PATH.append(neighbor)
            return temp
        if temp < minimum:
            minimum = temp

    return minimum


def biAstar(maze):
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

    calculate_f_cost(node=start_node, end=end_node)
    heapq.heappush(open_heap_start, start_node)
    open_dictionary_start[start_node] = True

    calculate_f_cost(node=end_node, end=start_node)
    heapq.heappush(open_heap_end, end_node)
    open_dictionary_end[end_node] = True

    current_node2 = end_node

    came_from_start = {}
    came_from_end = {}

    while len(open_heap_start) != 0 and len(open_heap_end) != 0:
        current_node = heapq.heappop(open_heap_start)
        current_node.make_closed()
        open_dictionary_start[current_node] = False
        closed_dictionary_start[current_node] = True
        draw_node(maze, current_node)
        if closed_dictionary_end.get(current_node, False):
            cost = current_node.get_g()
            current_node.make_grey()
            draw_node(maze, current_node)
            recreate_bidirectional_path(maze, current_node, came_from_start, came_from_end)
            return True
        biAstar_helper(maze, current_node, end_node, open_dictionary_start, closed_dictionary_start, came_from_start, open_heap_start)

        #   second one #######################
        current_node2 = heapq.heappop(open_heap_end)
        # current_node2.make_closed()
        current_node2.make_blue()
        open_dictionary_end[current_node2] = False
        closed_dictionary_end[current_node2] = True
        draw_node(maze, current_node2)
        if closed_dictionary_start.get(current_node2, False):
            cost = current_node2.get_g()
            current_node2.make_grey()
            draw_node(maze, current_node2)
            recreate_bidirectional_path(maze, current_node2, came_from_start, came_from_end)
            time_end = time.time()
            print("cost = ", cost)
            return True
        biAstar_helper(maze, current_node2, start_node, open_dictionary_end, closed_dictionary_end, came_from_end, open_heap_end)

    return False


def biAstar_helper(maze, current_node, end_node, open_dictionary, closed_dictionary, came_from, open_heap):
    for neighbor in current_node.get_neighbors():
        neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
        if open_dictionary.get(neighbor, False):
            if neighbor.get_g() <= neighbor_current_cost: continue
            neighbor.set_g(neighbor_current_cost)
            came_from[neighbor] = current_node
            calculate_f_cost(neighbor, end_node)
            heapq.heapify(open_heap)
            neighbor.make_open()
            draw_node(maze, neighbor)
        elif closed_dictionary.get(neighbor, False):
            if neighbor.get_g() <= neighbor_current_cost: continue
            closed_dictionary[neighbor] = False
            neighbor.set_g(neighbor_current_cost)
            came_from[neighbor] = current_node
            calculate_f_cost(neighbor, end_node)
            heapq.heapify(open_heap)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            draw_node(maze, neighbor)
        else:
            neighbor.set_g(neighbor_current_cost)
            came_from[neighbor] = current_node
            calculate_f_cost(neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            neighbor.make_open()
            open_dictionary[neighbor] = True
            draw_node(maze, neighbor)

def recreate_bidirectional_path(maze, node, came_from_start, came_from_end):
    node.make_path()
    draw_node(maze, node)

    node_x = node.get_x()
    node_y = node.get_y()

    while node in came_from_start:
        node = came_from_start[node]
        node.make_path()
        PATH.append(node)
        node.make_path()
        draw_node(maze, node)

    node = maze.get_grid()[node_x][node_y]

    while node in came_from_end:
        node = came_from_end[node]
        node.make_path()
        PATH.append(node)
        node.make_path()
        draw_node(maze, node)


def heuristic1(node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())

    return (dx + dy) * 1


def heuristic2(node, end):
    return 0
