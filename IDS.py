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

    maze.update_expanded_nodes()
    # Recur for all the vertices adjacent to this vertex
    neighbors = start.get_neighbors()
    for node in neighbors:
        if node in visited:
            if visited.get(node) <= steps:
                continue
        if (node.get_x(), node.get_y()) != maze.get_start():
            node.make_closed()
        # pygame.draw.rect(WINDOW, node.color, (
        #     node.get_y() * maze.get_square_size(), node.get_x() * maze.get_square_size(), maze.get_square_size(),
        #     maze.get_square_size()))
        # draw_grid(maze=maze)
        # pygame.display.update()
        visited[node] = steps
        if dls(node, end, max_depth - 1, maze, visited, steps + 1):
            node.make_path()
            # draw_node(maze, node)
            maze.get_path().append(node)
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
        visited = {start: 0}
        if dls(start=start, end=end, max_depth=depth, maze=maze, visited=visited, steps=0):
            time_end = time.time()
            maze.get_path().append(start)
            maze.print(time_end - time_start)
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