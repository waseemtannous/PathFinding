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

        self.solution_depth = 0
        self.avg_hval = []

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
        self.solution_depth = len(self.get_path()) - 1
        self.print_path()
        print("time in sec: ", time)
        print("N = ", self.number_of_expanded_nodes)
        print("d = ", self.solution_depth)
        print("EBF = ", pow(self.number_of_expanded_nodes, (1 / self.solution_depth)))
        avg_hval = 0
        sum = 0
        for num in self.avg_hval:
            sum += num
        if (self.algotype is AlgorithmType.ASTAR) or (self.algotype is AlgorithmType.IDASTAR) or (self.algotype is AlgorithmType.BIASTAR):
            avg_hval = sum / len(self.avg_hval)
            print("avg H value = ", avg_hval)


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
        print()
        print("cost = ", cost)

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
