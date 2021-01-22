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
        # the average value of the heuristic function
        self.sum_h_val = 0
        self.num_h_val = 0
        self.found = False  # found the goal or not

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
            self.found = True
            self.print()
        else:  # else print not found
            self.print_not_found()

    def print_not_found(self):
        f = open('output.txt', 'w')
        f.write('Not Found!')
        f.close()

    def print(self):  # this function prints all relevant stats about the algorithm
        self.solution_depth = len(self.get_path()) - 1
        path_string = self.print_path()
        stats_string = self.print_stats()
        f = open('output.txt', 'w')
        f.write(path_string)
        f.write(stats_string)
        f.close()

    def print_stats(self):
        dictionary = {1: 'Heuristic name', 2: 'N', 3: 'd/N', 4: 'Success(Y/N)',
                      5: 'Time(sec)', 6: 'EBF', 7: 'avg H value', 8: 'Min', 9: 'Avg', 10: 'Max'}
        ebf = pow(self.number_of_expanded_nodes, (1 / self.solution_depth))
        d_n = self.solution_depth / self.number_of_expanded_nodes
        avg_hval = None
        if self.num_h_val > 0:
            avg_hval = self.sum_h_val / self.num_h_val
        if self.number_cuttoff == 0:
            self.min_cuttoff = 0
            self.number_cuttoff = 1
        avg_tree_depth = self.sum_cuttoff / self.number_cuttoff

        heuristic_name = None
        if self.algotype == AlgorithmType.ASTAR or self.algotype == AlgorithmType.BIASTAR or self.algotype == AlgorithmType.IDASTAR:
            heuristic_name = 'Euclidean Distance'

        line1 = ''
        line2 = ''

        line1 += dictionary.get(1)
        line2 += str(heuristic_name)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(2)
        line2 += str(self.number_of_expanded_nodes)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(3)
        line2 += str(d_n)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(4)
        if self.found:
            line2 += 'Y'
        else:
            line2 += 'N'
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(5)
        line2 += str(self.actual_time)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(6)
        line2 += str(ebf)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(7)
        line2 += str(avg_hval)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(8)
        line2 += str(self.min_cuttoff)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(9)
        line2 += str(avg_tree_depth)
        line1, line2 = self.format_line(line1, line2)

        line1 += dictionary.get(10)
        line2 += str(self.max_cuttoff)
        line1, line2 = self.format_line(line1, line2)

        line1 += '\n'
        line2 += '\n'
        return '\n' + line1 + line2

    def format_line(self, line1, line2):
        if len(line1) > len(line2):
            for _ in range(len(line1) - len(line2)):
                line2 += ' '
        else:
            for _ in range(len(line2) - len(line1)):
                line1 += ' '
        line1 += '|'
        line2 += '|'

        return line1, line2

    def print_path(self):  # prints the path direction from start to the end node
        path = self.PATH
        node = path.pop()
        cost = 0
        string = ''
        while len(path) != 0:
            next_node = path.pop()
            cost += next_node.get_cost()
            if len(path) == 0:
                string += node.direction(next_node)
            else:
                string += (node.direction(next_node) + '-')
            node = next_node
        string += (' ' + str(cost))
        string += (' ' + str(self.number_of_expanded_nodes))
        string += '\n'
        return string

    def update_expanded_nodes(self):  # updates the number of the nodes we expanded
        self.number_of_expanded_nodes += 1

    def update_cuttoff(self, depth):  # updates when the algorithm makes a cuttoff
        self.min_cuttoff = min(self.min_cuttoff, depth)
        self.max_cuttoff = max(self.max_cuttoff, depth)
        self.sum_cuttoff += depth
        self.number_cuttoff += 1

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
