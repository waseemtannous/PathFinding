from Colors import *

class Node:
    def __init__(self, x, y, color, cost):
        self.x = x
        self.y = y
        self.color = color
        self.cost = cost
        self.neighbors = []

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

    def set_neighbors(self, maze):
        grid = maze.get_grid()
        self.neighbors = []
        if self.get_x() != 0 and not grid[self.get_x() - 1][self.get_y()].is_barier():    #up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y()])

        if self.get_x() < maze.get_size() - 1 and not grid[self.get_x() + 1][self.get_y()].is_barier():   #down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y()])

        if self.get_y() != 0 and not grid[self.get_x()][self.get_y() - 1].is_barier():    #left
            self.neighbors.append(grid[self.get_x()][self.get_y() - 1])

        if self.get_y() < maze.get_size() - 1 and not grid[self.get_x()][self.get_y() + 1].is_barier():    #right
            self.neighbors.append(grid[self.get_x()][self.get_y() + 1])

        if self.get_x() != 0 and self.get_y() < maze.get_size() - 1 and not grid[self.get_x() - 1][self.get_y() + 1].is_barier():    #right up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() + 1])

        if self.get_x() < maze.get_size() - 1 and self.get_y() < maze.get_size() and not grid[self.get_x() + 1][self.get_y() + 1].is_barier():    #right down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y() + 1])

        if self.get_y() != 0 and self.get_x() != 0 and not grid[self.get_x() - 1][self.get_y() - 1].is_barier():    #left up
            self.neighbors.append(grid[self.get_x() - 1][self.get_y() - 1])

        if self.get_y() != 0 and self.get_x() < maze.get_size() - 1 and not grid[self.get_x() + 1][self.get_y() - 1].is_barier():    #left down
            self.neighbors.append(grid[self.get_x() + 1][self.get_y() - 1])

