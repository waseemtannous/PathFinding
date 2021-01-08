from AlgorithmType import *

import ASTAR
import IDS
import BIASTAR
import UCS
import IDASTAR


class Maze:
    def __init__(self, algotype, size, start, end, matrix):
        self.grid = None
        self.square_size = None
        self.algotype = algotype
        self.size = size
        self.start = start
        self.end = end
        self.matrix = matrix
        self.PATH = []
        self.number_of_expanded_nodes = 0

    def run(self):
        if self.algotype == AlgorithmType.ASTAR:
            ASTAR.draw(self)
            ASTAR.astar(self)
        elif self.algotype == AlgorithmType.IDASTAR:
            IDASTAR.draw(self)
            IDASTAR.idAstar(self)
        elif self.algotype == AlgorithmType.UCS:
            UCS.draw(self)
            UCS.ucs(self)
        elif self.algotype == AlgorithmType.IDS:
            IDS.draw(self)
            IDS.ids(self)
        elif self.algotype == AlgorithmType.BIASTAR:
            BIASTAR.draw(self)
            BIASTAR.biAstar(self)

    def print(self, time):
        self.print_path()
        print(self.number_of_expanded_nodes, end=" ")
        print("time in sec: ", time)

    def print_path(self):
        path = self.get_path()
        node = path.pop()
        cost = 0
        print(len(path))
        while len(path) != 0:
            next_node = path.pop()
            cost += next_node.get_cost()
            if len(path) == 0:
                print(node.direction(next_node), end="")
            else:
                print(node.direction(next_node), "-", end="")
            node = next_node
        print(" ", cost, end=" ")

    def update_expanded_nodes(self):
        self.number_of_expanded_nodes += 1

    def get_path(self):
        return self.PATH

    def get_size(self):
        return self.size

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_matrix(self):
        return self.matrix

    def set_grid(self, grid):
        self.grid = grid

    def set_square_size(self, square_size):
        self.square_size = square_size

    def get_square_size(self):
        return self.square_size

    def get_grid(self):
        return self.grid
