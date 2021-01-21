import time
import math


def ids(maze):
    # set maximum run time
    maze.max_time = math.sqrt(maze.size)
    # maze.max_time = maze.size
    # maze.max_time = 10000
    # maze.max_time = 0.8
    grid = maze.get_grid()
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    # get start and end nodes
    start = grid[x1][y1]
    end = grid[x2][y2]
    max_depth = maze.size * maze.size
    time_start = time.time()
    # depth limit search till max depth
    for depth in range(max_depth):
        # check if time has ended
        if not (time.time() - time_start <= maze.max_time):
            return False
        visited = {start: 0}
        if dls(current_node=start, end=end, max_depth=depth, maze=maze, visited=visited, time_start=time_start):
            maze.actual_time = time.time() - time_start
            maze.get_path().append(start)
            return True
    return False


# depth limited search
def dls(current_node, end, max_depth, maze, visited, time_start):
    # check if time has ended
    if not (time.time() - time_start <= maze.max_time):
        return False

    # check if current node is the end node
    if current_node == end:
        maze.update_cuttoff(current_node.depth)
        return True

    # if reached the maximum depth, stop recursing.
    if max_depth <= 0:
        maze.update_cuttoff(current_node.depth)
        return False

    maze.update_expanded_nodes()

    # recurse for all the neighbors
    neighbors = current_node.get_neighbors()
    for node in neighbors:
        current_cost = current_node.get_g() + node.get_cost()
        # check if we have reached this node in less g cost
        if visited.get(node, False):
            if node.get_g() <= current_cost:
                continue

        node.set_depth(current_node.get_depth())
        node.set_parent(current_node)
        visited[node] = True
        node.set_g(current_cost)
        if dls(node, end, max_depth - 1, maze, visited, time_start):
            maze.get_path().append(node)
            return True
    maze.update_cuttoff(current_node.depth)
    return False
