import math


def calculate_f_cost(maze, node, end):
    heuristic = heuristic1(maze, node=node, end=end)
    node.set_h(heuristic)
    node.calculate_f()


def heuristic1(maze, node, end):
    dx = abs(node.get_x() - end.get_x())
    dy = abs(node.get_y() - end.get_y())

    d1 = 1
    d2 = math.sqrt(2)
    d2 = 1

    retval = (dx + dy) * 1

    # return (d1 * (dx + dy)) + ((d2 - (2 * d1)) * min(dx, dy))

    maze.avg_hval.append(retval)

    return retval
    # if dx > dy:
    #     return (14 * dy) + (10 * (dx - dy))
    # else:
    #     return (14 * dx) + (10 * (dy - dx))


def heuristic2(node, end):
    return 0
