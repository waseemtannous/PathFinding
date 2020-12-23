from queue import PriorityQueue

import pygame

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


def recreate_path(maze):
    for node in PATH:
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()


def astar(maze):
    pass


# depth limited search
def dls(start, end, max_depth, maze, visited):
    if start == end: return True

    # If reached the maximum depth, stop recursing.
    if max_depth <= 0: return False

    for node in start.get_neighbors():
        if visited.get((node, max_depth), False):
            continue
        node.make_open()
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()

    # Recur for all the vertices adjacent to this vertex
    for node in start.get_neighbors():
        if visited.get((node, max_depth), False):
        
            continue
        if (node.get_x(), node.get_y()) != maze.get_start():
            node.make_closed()
        pygame.draw.rect(WINDOW, node.color, (
            node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
            maze.get_square_size()))
        draw_grid(maze=maze)
        pygame.display.update()
        visited[node] = True
        if dls(node, end, max_depth - 1, maze, visited):
            node.make_path()
            PATH.append(node)
            return True
    return False


# def dls(start, end, max_depth, maze):
#     d = 0
#     global to_visit
#     global expanded_nodes
#     global visited_nodes
#     to_visit.append(start)
#     expanded_nodes.append(start)
#
#     while len(to_visit) != 0:
#         current_node = to_visit.pop()
#         visited_nodes.append(current_node)
#         current_node.make_closed()
#         pygame.draw.rect(WINDOW, current_node.color, (
#             current_node.get_y() * maze.get_square_size(), current_node.get_x() * maze.get_square_size(),
#             maze.get_square_size(),
#             maze.get_square_size()))
#         draw_grid(maze=maze)
#         pygame.display.update()
#         if current_node == end:
#             return True
#         elif d < max_depth:
#             for neighbor in current_node.get_neighbors():
#                 expanded_nodes.append(neighbor)
#                 to_visit.append(neighbor)
#                 neighbor.make_open()
#                 pygame.draw.rect(WINDOW, neighbor.color, (
#                     neighbor.get_y() * maze.get_square_size(), neighbor.get_x() * maze.get_square_size(),
#                     maze.get_square_size(),
#                     maze.get_square_size()))
#                 draw_grid(maze=maze)
#                 pygame.display.update()
#             d += 1
#     return False

def ids(maze):
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    start = grid[x1][y1]
    end = grid[x2][y2]
    # depth limit search till max depth
    max_depth = 100
    for depth in range(max_depth):
        print("iter ", depth)
        visited = {(start, 0) : True}
        if dls(start=start, end=end, max_depth=depth, maze=maze, visited=visited):
            recreate_path(maze)
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
    pass


def biAstar(maze):
    pass


def heuristic1():
    return 0


def heuristic2():
    return 0
