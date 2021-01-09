


class Node:
    def __init__(self, x, y, cost):
        self.parent = None
        self.x = x
        self.y = y
        # self.color = color
        self.cost = cost
        self.neighbors = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.visited = False
        self.visited_from_end = False

        self.tree_neighbors = []

    def is_visited(self):
        return self.visited

    def is_visited_from_end(self):
        return self.visited_from_end

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_cost(self):
        return self.cost

    def get_position(self):
        return self.x, self.y

    def get_neighbors(self):
        return self.neighbors

    def get_h(self):
        return self.h

    def get_f(self):
        return self.f

    def set_h(self, h):
        self.h = h

    def get_g(self):
        return self.g

    def set_g(self, g):
        self.g = g

    def calculate_f(self):
        self.f = self.g + self.h

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def set_neighbors(self, maze):
        grid = maze.get_grid()
        self.neighbors = []
        if self.get_x() != 0 and not (grid[self.get_x() - 1][self.get_y()].get_cost() == -1):  # up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y()])

        if self.get_x() < maze.get_size() - 1 and not (grid[self.get_x() + 1][self.get_y()].get_cost() == -1):  # down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y()])

        if self.get_y() != 0 and not (grid[self.get_x()][self.get_y() - 1].get_cost() == -1):  # left
            self.neighbors.append(grid[self.get_x()][self.get_y() - 1])

        if self.get_y() < maze.get_size() - 1 and not (grid[self.get_x()][self.get_y() + 1].get_cost() == -1):  # right
            self.neighbors.append(grid[self.get_x()][self.get_y() + 1])

        if self.get_x() != 0 and self.get_y() < maze.get_size() - 1 and not (grid[self.get_x() - 1][self.get_y() + 1].get_cost() == -1):  # right up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() + 1])

        if self.get_x() < maze.get_size() - 1 and self.get_y() < maze.get_size() - 1 and not (grid[self.get_x() + 1][self.get_y() + 1].get_cost() == -1):  # right down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y() + 1])

        if self.get_y() != 0 and self.get_x() != 0 and not (grid[self.get_x() - 1][self.get_y() - 1].get_cost() == -1):  # left up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() - 1])

        if self.get_y() != 0 and self.get_x() < maze.get_size() - 1 and not (grid[self.get_x() + 1][self.get_y() - 1].get_cost() == -1):  # left down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y() - 1])

        # self.neighbors.sort(key=get_cost)

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __gt__(self, other):
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    def direction(self, other):  # self = parent, other = neighbor
        dx = other.get_x() - self.get_x()
        dy = other.get_y() - self.get_y()

        if dx == -1 and dy == 0:
            return "U"
        if dx == -1 and dy == 1:
            return "RU"
        if dx == 0 and dy == 1:
            return "R"
        if dx == 1 and dy == 1:
            return "RD"
        if dx == 1 and dy == 0:
            return "D"
        if dx == 1 and dy == -1:
            return "LD"
        if dx == 0 and dy == -1:
            return "L"
        if dx == -1 and dy == -1:
            return "LU"


def get_cost(node):
    return node.get_cost()
