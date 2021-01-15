from AlgorithmType import *

import ASTAR
import IDS
import BIASTAR
import UCS
import IDASTAR


class Maze:
    def __init__(self, algotype, size, start, end, matrix):
        self.grid = None
        self.second_grid = None
        self.square_size = None
        self.algotype = algotype
        self.size = size
        self.start = start
        self.end = end
        self.matrix = matrix
        self.PATH = []
        self.number_of_expanded_nodes = 0
        self.found = False
        self.running = True
        self.min_cuttoff = float('inf')
        self.max_cuttoff = (-1) * float('inf')
        self.sum_cuttoff = 0
        self.number_cuttoff = 0
        self.max_time = 0
        self.actual_time = 0


        self.solution_depth = 0
        self.avg_hval = []
        self.depth_array = []

    def run(self):
        result = False
        if self.algotype == AlgorithmType.ASTAR:
            ASTAR.draw(self)
            result = ASTAR.astar(self)
        elif self.algotype == AlgorithmType.IDASTAR:
            IDASTAR.draw(self)
            result = IDASTAR.idAstar(self)
        elif self.algotype == AlgorithmType.UCS:
            UCS.draw(self)
            result = UCS.ucs(self)
        elif self.algotype == AlgorithmType.IDS:
            IDS.draw(self)
            result = IDS.ids(self)
        elif self.algotype == AlgorithmType.BIASTAR:
            BIASTAR.draw(self)
            result = BIASTAR.biAstar(self)
        if result:
            self.print()
        else:
            self.print_not_found()


    def print_not_found(self):
        print("Not Found!")


    def print(self):
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
        if (self.algotype is AlgorithmType.ASTAR) or (self.algotype is AlgorithmType.IDASTAR) or (self.algotype is AlgorithmType.BIASTAR):
            avg_hval = sum / len(self.avg_hval)
            print("avg H value = ", avg_hval)
        self.print_cuttoff()



    def tree_stats(self):
        root = self.get_grid()[self.start[0]][self.start[1]]
        dls(self, root, 0)

        minimum = float('inf')
        maximum = (-1) * float('inf')
        sum = 0

        for num in self.depth_array:
            sum += num
            maximum = max(num, maximum)
            minimum = min(num, minimum)
        average = sum / len(self.depth_array)

        print("min tree depth = ", minimum)
        print("max tree depth = ", maximum)
        print("avg tree depth = ", average)


    def print_path(self):
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

    def update_expanded_nodes(self):
        self.number_of_expanded_nodes += 1

    def update_cuttoff(self, depth):
        self.min_cuttoff = min(self.min_cuttoff, depth)
        self.max_cuttoff = max(self.max_cuttoff, depth)
        self.sum_cuttoff += depth
        self.number_cuttoff += 1

    def print_cuttoff(self):
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

    def set_square_size(self, square_size):
        self.square_size = square_size

    def get_square_size(self):
        return self.square_size




def dls(maze, root, depth):
    if len(root.tree_neighbors) == 0:
        maze.depth_array.append(depth)
        return

    neighbors = root.tree_neighbors
    for node in neighbors:
        dls(maze, node, depth + 1)