import math

# calculates the heuristic and updates the f_cost of the node
def calculate_f_cost(maze, node, end):
    heuristic = max(heuristic2(maze, node, end), heuristic3(maze, node, end))
    # heuristic = heuristic2(maze, node, end)
    node.set_h(heuristic)
    node.calculate_f()


# def heuristic1(maze, node, end):
#     dx = abs(node.get_x() - end.get_x())
#     dy = abs(node.get_y() - end.get_y())
#
#     d1 = 1
#     d2 = math.sqrt(2)
#     d2 = 1
#
#     retval = (dx + dy) * 1
#
#     # return (d1 * (dx + dy)) + ((d2 - (2 * d1)) * min(dx, dy))
#
#     maze.avg_hval.append(retval)
#
#     return retval
#     # return 0
#     # if dx > dy:
#     #     return (14 * dy) + (10 * (dx - dy))
#     # else:
#     #     return (14 * dx) + (10 * (dy - dx))


def heuristic2(maze, node, end):  # euclidean distance
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())

    D = float('inf')

    neighbors = node.get_neighbors()
    # for neighbor in neighbors:
    #     D = min(D, neighbor.get_cost())

    retval = 1 * math.sqrt((dx * dx) + (dy * dy))
    # retval = (dx + dy)
    maze.avg_hval.append(retval)

    return retval


def heuristic1(maze, node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())
    D = float('inf')
    D2 = float('inf')
    neighbors = node.get_neighbors()
    for neighbor in neighbors:
        D = min(D, neighbor.get_cost())
        if not ((neighbor.get_x() == node.get_x()) or (neighbor.get_y() == node.get_y())):
            D2 = min(D2, neighbor.get_cost())
    if D2 == float('inf'):
        D2 = D
    ret_val = (D * (dx + dy)) + ((D2 - (2 * D)) * min(dx, dy))
    maze.avg_hval.append(ret_val)
    return ret_val


def heuristic3(maze, node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())

    D = node.min_neighbor_cost
    D2 = node.min_diagonal_neighbor_cost

    retval = D2 + (D * (abs(dx - dy)))
    # retval = (dx + dy)
    maze.avg_hval.append(retval)

    return retval