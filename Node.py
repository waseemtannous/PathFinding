from Colors import *

class Node:
    def __init__(self, x, y, color, cost):
        self.parent = None
        self.x = x
        self.y = y
        self.color = color
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

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

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
        if self.get_x() != 0 and not grid[self.get_x() - 1][self.get_y()].is_barrier():    #up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y()])

        if self.get_x() < maze.get_size() - 1 and not grid[self.get_x() + 1][self.get_y()].is_barrier():   #down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y()])

        if self.get_y() != 0 and not grid[self.get_x()][self.get_y() - 1].is_barrier():    #left
            self.neighbors.append(grid[self.get_x()][self.get_y() - 1])

        if self.get_y() < maze.get_size() - 1 and not grid[self.get_x()][self.get_y() + 1].is_barrier():    #right
            self.neighbors.append(grid[self.get_x()][self.get_y() + 1])

        if self.get_x() != 0 and self.get_y() < maze.get_size() - 1 and not grid[self.get_x() - 1][self.get_y() + 1].is_barrier():    #right up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() + 1])

        if self.get_x() < maze.get_size() - 1 and self.get_y() < maze.get_size() - 1 and not grid[self.get_x() + 1][self.get_y() + 1].is_barrier():    #right down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y() + 1])

        if self.get_y() != 0 and self.get_x() != 0 and not grid[self.get_x() - 1][self.get_y() - 1].is_barrier():    #left up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() - 1])

        if self.get_y() != 0 and self.get_x() < maze.get_size() - 1 and not grid[self.get_x() + 1][self.get_y() - 1].is_barrier():    #left down
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

    def make_yellow(self):
        self.color = YELLOW
    def make_blue(self):
        self.color = BLUE

    def make_grey(self):
        self.color = GREY

    def direction(self, other): # self = parent, other = neighbor
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