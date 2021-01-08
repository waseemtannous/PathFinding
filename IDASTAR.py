import pygame
from Colors import *
from Heuristics import *
import time


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


def idAstar(maze):
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    calculate_f_cost(maze, start_node, end_node)
    threshold = start_node.get_f()

    time_start = time.time()

    while threshold < float('inf') and maze.running:
        visited = {}
        visited[start_node] = 0
        temp = idastar_helper(maze, start_node, end_node, threshold, visited)
        if temp < 0:
            print("found")
            while end_node.get_parent() is not None:
                maze.get_path().append(end_node)
                end_node.make_path()
                # draw_node(maze, end_node)
                end_node = end_node.get_parent()
            maze.get_path().append(start_node)
            time_end = time.time()
            maze.print(time_end - time_start)
            return True
        elif temp == float("inf"):
            print("not found")
            return False
        else:
            # for row in maze.get_grid():
            #     for node in row:
            #         if node.get_cost() == 0:
            #             node.make_barrier()
            #         elif node == start_node:
            #             node.make_start()
            #         elif node == end_node:
            #             node.make_end()
            #         else:
            #             node.reset()
            #         pygame.draw.rect(WINDOW, node.color, (
            #             node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(),
            #             maze.get_square_size(),
            #             maze.get_square_size()))
            # start_node.make_start()
            # end_node.make_end()
            # draw_grid(maze=maze)
            # pygame.display.update()
            threshold = temp


def idastar_helper(maze, node, end_node, threshold, visited):
    if not maze.running:
        return False
    node.make_closed()
    maze.update_expanded_nodes()
    # draw_node(maze, node)
    if (node.get_x(), node.get_y()) == (end_node.get_x(), end_node.get_y()):
        return -1

    fn = float("inf")
    neighbors = node.get_neighbors()
    for neighbor in neighbors:
        current_cost = node.get_g() + neighbor.get_cost()
        if neighbor in visited:
            if visited.get(neighbor) <= current_cost:
                continue
        visited[neighbor] = current_cost
        neighbor.set_g(current_cost)
        calculate_f_cost(maze, neighbor, end_node)
        neighbor.set_parent(node)
        neighbor.make_open()
        # draw_node(maze, neighbor)
        f = neighbor.get_f()
        if f <= threshold:
            fn = min(fn, idastar_helper(maze, neighbor, end_node, threshold, visited))
        else:
            fn = min(fn, f)
    return fn