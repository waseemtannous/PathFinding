from AlgorithmType import *
import Algorithms


class Maze:
    def __init__(self, algotype, size, start, end, matrix):
        self.grid = None
        self.square_size = None
        self.algotype = algotype
        self.size = size
        self.start = start
        self.end = end
        self.matrix = matrix

    def run(self):
        if self.algotype == AlgorithmType.ASTAR:
            Algorithms.astar(self)
        elif self.algotype == AlgorithmType.IDASTAR:
            Algorithms.idAstar(self)
        elif self.algotype == AlgorithmType.UCS:
            Algorithms.ucs(self)
        elif self.algotype == AlgorithmType.IDS:
            Algorithms.ids(self)
        elif self.algotype == AlgorithmType.BIASTAR:
            Algorithms.biAstar(self)

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