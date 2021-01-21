import math


# calculates the heuristic and updates the f_cost of the node
def calculate_f_cost(maze, node, end):
    heuristic = euclidean_distance(node, end)
    # heuristic = octile_distance(node, end)
    # heuristic = chebyshev_distance(node, end)
    # heuristic = max_heuristic(node, end)
    maze.avg_hval.append(heuristic)
    node.set_h(heuristic)
    node.calculate_f()


def euclidean_distance(node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())
    return math.sqrt((dx * dx) + (dy * dy))


def chebyshev_distance(node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())
    return max(dx, dy) - min(dx, dy)


def octile_distance(node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())
    return max(dx, dy) - (0.5858 * min(dx, dy))


def max_heuristic(node, end):
    return max(octile_distance(node, end),
               chebyshev_distance(node, end),
               euclidean_distance(node, end))
