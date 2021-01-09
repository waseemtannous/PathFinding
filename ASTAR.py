import time
import heapq
from Heuristics import *


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
        open_dictionary[current_node] = False
        closed_dictionary[current_node] = True

        if current_node.get_parent() is not None:  # tree
            current_node.get_parent().tree_neighbors.append(current_node)

        if current_node.get_x() == end_node.get_x() and current_node.get_y() == end_node.get_y():
            maze.found = True
            maze.running = False
            time_end = time.time()
            while current_node.get_parent() is not None:
                maze.get_path().append(current_node)
                current_node = current_node.get_parent()
            maze.get_path().append(start_node)
            maze.time = time_end - time_start
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
            elif closed_dictionary.get(neighbor, False):
                if neighbor.get_g() <= neighbor_current_cost:
                    continue
                closed_dictionary[neighbor] = False
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                open_dictionary[neighbor] = True
            else:
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                open_dictionary[neighbor] = True

    maze.running = False
    return False
