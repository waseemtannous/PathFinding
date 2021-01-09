import time


# depth limited search
def dls(start, end, max_depth, maze, visited, steps):
    if not maze.running:
        return False
    if start.get_parent() is not None:  # tree
        start.get_parent().tree_neighbors.append(start)

    if start == end:
        return True

    # If reached the maximum depth, stop recursing.
    if max_depth <= 0:
        return False

    maze.update_expanded_nodes()
    # Recur for all the vertices adjacent to this vertex
    neighbors = start.get_neighbors()
    for node in neighbors:
        if node in visited:
            if visited.get(node) <= steps:
                continue
        node.set_parent(start)
        visited[node] = steps
        if dls(node, end, max_depth - 1, maze, visited, steps + 1):
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
        if not maze.running:
            return False
        visited = {start: 0}
        if dls(start=start, end=end, max_depth=depth, maze=maze, visited=visited, steps=0):
            time_end = time.time()
            maze.get_path().append(start)
            maze.print(time_end - time_start)
            return True
    time_end = time.time()
    print("time in sec: ", time_end - time_start)
    return False
