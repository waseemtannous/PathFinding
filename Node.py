class Node:
    def __init__(self, x, y, cost):
        self.parent = None
        self.x = x
        self.y = y
        self.cost = cost
        self.neighbors = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.depth = 0

    def get_depth(self):
        return self.depth

    def set_depth(self, depth):
        self.depth = depth + 1

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

    # checks if other node is a neighbor of this node
    def is_neighbor(self, other):
        for neighbor in self.neighbors:
            if neighbor.get_x() == other.get_x() and neighbor.get_y() == other.get_y():
                return True
        return False

    def set_neighbors(self, maze, grid):
        self.neighbors = []
        if self.get_x() != 0 and not (grid[self.get_x() - 1][self.get_y()].get_cost() == -1):  # up
            node = grid[self.get_x() - 1][self.get_y()]
            self.neighbors.append(node)

        if self.get_x() < maze.get_size() - 1 and not (grid[self.get_x() + 1][self.get_y()].get_cost() == -1):  # down
            node = grid[self.get_x() + 1][self.get_y()]
            self.neighbors.append(node)

        if self.get_y() != 0 and not (grid[self.get_x()][self.get_y() - 1].get_cost() == -1):  # left
            node = grid[self.get_x()][self.get_y() - 1]
            self.neighbors.append(node)

        if self.get_y() < maze.get_size() - 1 and not (grid[self.get_x()][self.get_y() + 1].get_cost() == -1):  # right
            node = grid[self.get_x()][self.get_y() + 1]
            self.neighbors.append(node)

        if self.get_x() != 0 and self.get_y() < maze.get_size() - 1 and not (
                grid[self.get_x() - 1][self.get_y() + 1].get_cost() == -1):  # right up
            node = grid[self.get_x() - 1][self.get_y() + 1]
            self.neighbors.append(node)

        if self.get_x() < maze.get_size() - 1 and self.get_y() < maze.get_size() - 1 and not (
                grid[self.get_x() + 1][self.get_y() + 1].get_cost() == -1):  # right down
            node = grid[self.get_x() + 1][self.get_y() + 1]
            self.neighbors.append(node)

        if self.get_y() != 0 and self.get_x() != 0 and not (
                grid[self.get_x() - 1][self.get_y() - 1].get_cost() == -1):  # left up
            node = grid[self.get_x() - 1][self.get_y() - 1]
            self.neighbors.append(node)

        if self.get_y() != 0 and self.get_x() < maze.get_size() - 1 and not (
                grid[self.get_x() + 1][self.get_y() - 1].get_cost() == -1):  # left down
            node = grid[self.get_x() + 1][self.get_y() - 1]
            self.neighbors.append(node)

    # these will determine how the heap will sort the nodes
    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __gt__(self, other):
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    # determine which direction to get from this node to other
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
