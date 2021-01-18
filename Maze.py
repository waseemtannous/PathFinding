from AlgorithmType import *

import ASTAR
import IDS
import BIASTAR
import UCS
import IDASTAR


class Maze:
    def __init__(self, algotype, size, start, end, matrix):
        self.grid = None  # this grid holds all the nodes
        self.second_grid = None  # this grid holds all the nodes and it hepls us in the biastar algorithm
        self.algotype = algotype  # enum whick indicates which algorithm we are running
        self.size = size  # matrix dimension
        self.start = start  # start node coordinates
        self.end = end  # end node coordinates
        self.matrix = matrix  # the cost matrix
        self.PATH = []  # holds the path from start to end
        self.number_of_expanded_nodes = 0  # N: this will be the number of nodes we expanded during an algorithm
        # minimum, maximum and avg depth at which the algorithm cut the path and jumped to another
        self.min_cuttoff = float('inf')
        self.max_cuttoff = (-1) * float('inf')
        self.sum_cuttoff = 0
        self.number_cuttoff = 0
        self.max_time = 0  # the maximum time an algorithm is allowed to run
        self.actual_time = 0  # the actual time it took the algorithm to find the path
        self.solution_depth = 0  # the depth of the end node
        self.avg_hval = []  # the average value of the heuristic function

    def run(self):  # this function runs the specified algorithm
        result = False
        if self.algotype == AlgorithmType.ASTAR:
            result = ASTAR.astar(self)
        elif self.algotype == AlgorithmType.IDASTAR:
            result = IDASTAR.idAstar(self)
        elif self.algotype == AlgorithmType.UCS:
            result = UCS.ucs(self)
        elif self.algotype == AlgorithmType.IDS:
            result = IDS.ids(self)
        elif self.algotype == AlgorithmType.BIASTAR:
            result = BIASTAR.biAstar(self)
        if result:  # if the path was found print it
            self.print()
        else:  # else print not found
            self.print_not_found()

    def print_not_found(self):
        print("Not Found!")

    def print(self):  # this function prints all relevant stats about the algorithm
        self.solution_depth = len(self.get_path()) - 1
        self.print_path()
        ebf = pow(self.number_of_expanded_nodes, (1 / self.solution_depth))
        print("time in sec: ", self.actual_time)
        print("N = ", self.number_of_expanded_nodes)
        print("d = ", self.solution_depth)
        print("EBF = ", ebf)
        sum = 0
        for num in self.avg_hval:
            sum += num
        if (self.algotype is AlgorithmType.ASTAR) or (self.algotype is AlgorithmType.IDASTAR) or (
                self.algotype is AlgorithmType.BIASTAR):
            avg_hval = sum / len(self.avg_hval)
            print("avg H value = ", avg_hval)
        self.print_cuttoff()

    def print_path(self):  # prints the path direction from start to the end node
        path = self.PATH
        node = path.pop()
        cost = 0
        print('path length: ' + str(len(path)))
        while len(path) != 0:
            next_node = path.pop()
            cost += next_node.get_cost()
            if len(path) == 0:
                print(node.direction(next_node), end='')
            else:
                print(node.direction(next_node) + '-', end='')
            node = next_node
        print(' ' + str(cost), end='')
        print(' ' + str(self.number_of_expanded_nodes))

    def update_expanded_nodes(self):  # updates the number of the nodes we expanded
        self.number_of_expanded_nodes += 1

    def update_cuttoff(self, depth):  # updates when the algorithm makes a cuttoff
        self.min_cuttoff = min(self.min_cuttoff, depth)
        self.max_cuttoff = max(self.max_cuttoff, depth)
        self.sum_cuttoff += depth
        self.number_cuttoff += 1

    def print_cuttoff(self):  # print the cuttoff stats
        if self.number_cuttoff == 0:
            self.min_cuttoff = 0
            self.min_cuttoff = 0
            self.number_cuttoff = 1
        print("min tree depth = ", self.min_cuttoff)
        print("max tree depth = ", self.max_cuttoff)
        print("avg tree depth = ", (self.sum_cuttoff / self.number_cuttoff))

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

    def get_grid(self):
        return self.grid

    def set_second_grid(self, second_grid):
        self.second_grid = second_grid

    def get_second_grid(self):
        return self.second_grid
