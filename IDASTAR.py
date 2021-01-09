from Heuristics import *
import time


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
            time_end = time.time()
            while end_node.get_parent() is not None:
                maze.get_path().append(end_node)
                end_node = end_node.get_parent()
            maze.get_path().append(start_node)
            maze.time = time_end - time_start
            return True
        elif temp == float("inf"):
            return False
        else:
            threshold = temp


def idastar_helper(maze, node, end_node, threshold, visited):
    if not maze.running:
        return False
    maze.update_expanded_nodes()
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
        f = neighbor.get_f()
        if f <= threshold:
            fn = min(fn, idastar_helper(maze, neighbor, end_node, threshold, visited))
        else:
            fn = min(fn, f)
    return fn
