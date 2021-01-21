from Heuristics import *
import time


def idAstar(maze):
    # set maximum run time
    # maze.max_time = math.sqrt(maze.size)
    maze.max_time = 1000
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    # get start and end nodes
    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    # the starting threashold is the f_cost of start node
    calculate_f_cost(maze, start_node, end_node)
    threshold = start_node.get_f()
    print("threashold: ", threshold)

    time_start = time.time()

    while threshold < float('inf'):
        visited = {start_node: True}
        # temp will be the next threashold
        temp = idastar_helper(maze, start_node, end_node, threshold, visited, time_start)
        if temp == -1:
            maze.actual_time = time.time() - time_start
            # loop to make the path
            while end_node.get_parent() is not None:
                maze.get_path().append(end_node)
                end_node = end_node.get_parent()
            maze.get_path().append(start_node)
            return True
        elif temp == -2:
            return False
        else:
            # update the threashold
            threshold = temp
            # print(threshold)


def idastar_helper(maze, node, end_node, threshold, visited, time_start):
    # check if time has finished
    if not (time.time() - time_start <= maze.max_time):
        return -2

    maze.update_expanded_nodes()

    # check if this is the end node
    if (node.get_x(), node.get_y()) == (end_node.get_x(), end_node.get_y()):
        maze.update_cuttoff(node.get_depth())
        return -1

    fn = float('inf')
    neighbors = node.get_neighbors()

    # recurse for all neighbors
    for neighbor in neighbors:
        if fn == -1:
            return -1
        current_cost = node.get_g() + neighbor.get_cost()
        if visited.get(neighbor, False):
            # check if we visited this node in less g_cost
            if neighbor.get_g() <= current_cost:
                continue
        visited[neighbor] = True
        neighbor.set_g(current_cost)
        neighbor.set_depth(node.get_depth())
        calculate_f_cost(maze, neighbor, end_node)
        neighbor.set_parent(node)
        f = neighbor.get_f()
        # update the threashold
        if f <= threshold:
            fn = min(fn, idastar_helper(maze, neighbor, end_node, threshold, visited, time_start))
            maze.update_cuttoff(node.get_depth())
        else:
            fn = min(fn, f)
            maze.update_cuttoff(node.get_depth())
    # this returns the next threashold
    return fn




# def idastar_helper2(maze, node, end_node, visited, time_start):
#     global threashold
#     global next_threashold
#     global time_end
#     global found
#     # check if time has finished
#     if not (time.time() - time_start <= maze.max_time):
#         time_end = True
#         return
#
#     maze.update_expanded_nodes()
#
#     # check if this is the end node
#     if (node.get_x(), node.get_y()) == (end_node.get_x(), end_node.get_y()):
#         maze.update_cuttoff(node.get_depth())
#         found = True
#         return
#
#     fn = float('inf')
#     neighbors = node.get_neighbors()
#
#     # recurse for all neighbors
#     for neighbor in neighbors:
#         if found or time_end:
#             return
#         current_cost = node.get_g() + neighbor.get_cost()
#         if visited.get(neighbor, False):
#             # check if we visited this node in less g_cost
#             if neighbor.get_g() <= current_cost:
#                 continue
#         visited[neighbor] = True
#         neighbor.set_g(current_cost)
#         neighbor.set_depth(node.get_depth())
#         calculate_f_cost(maze, neighbor, end_node)
#         neighbor.set_parent(node)
#         f = neighbor.get_f()
#         if f <= threashold:
#             idastar_helper2(maze, neighbor, end_node, visited, time_start)
#         else:
#             next_threashold = min(f, next_threashold)

