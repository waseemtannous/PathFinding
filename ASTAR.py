import time
import heapq
from Heuristics import *


def astar(maze):
    maze.max_time = 2 * math.sqrt(maze.size)
    time_start = time.time()

    # Min heap for choosing the minimum cost every time.
    open_heap = []

    # Two hash tabels, open list (neighbors of the expanded node) and close list (contains expanded nodes) ,
    # O(1) time complixty for finding an item in the table
    open_dictionary = {}
    closed_dictionary = {}

    # Getting the coordinates of start node and the goal node
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()

    # Getting start node and the goal node
    start_node = maze.get_grid()[x1][y1]
    end_node = maze.get_grid()[x2][y2]

    # We calculate the F value for the node
    calculate_f_cost(maze, node=start_node, end=end_node)
    # Push the start node to the min heap and
    # put in the open list (open_dictionary)
    heapq.heappush(open_heap, start_node)
    open_dictionary[start_node] = True

    previous_node = None
    # While the open list is not empty and we are not out of time continue
    while len(open_heap) != 0 and (time.time() - time_start <= maze.max_time):
        # We get the node with minimal cost
        current_node = heapq.heappop(open_heap)
        maze.update_expanded_nodes()
        # Remove the node from the open list ,and add it to the close list
        open_dictionary[current_node] = False
        closed_dictionary[current_node] = True

        if previous_node:
            if not previous_node.is_neighbor(current_node):
                maze.update_cuttoff(previous_node.depth)

        previous_node = current_node
        # The GOAL node has been found ENTER HERE!
        if current_node.get_x() == end_node.get_x() and current_node.get_y() == end_node.get_y():
            maze.actual_time = time.time() - time_start
            maze.update_cuttoff(current_node.depth)
            while current_node.get_parent() is not None:
                # Add the node to the path
                maze.get_path().append(current_node)
                current_node = current_node.get_parent()
            maze.get_path().append(start_node)
            return True
        # Expanding the node and getting its neighbors
        neighbors = current_node.get_neighbors()
        for neighbor in neighbors:
            # Updating the cost
            neighbor_current_cost = current_node.get_g() + neighbor.get_cost()
            # If the node is already on the open list ENTER HERE
            if open_dictionary.get(neighbor, False):
                # If the cost is larger then do nothing
                if neighbor.get_g() <= neighbor_current_cost:
                    continue
                # Else if the cost is smaller update the node with the new one
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_depth(current_node.get_depth())
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heapify(open_heap)
            # If the node is on the close list ENTER HERE
            elif closed_dictionary.get(neighbor, False):
                # If the cost is larger then do nothing
                if neighbor.get_g() <= neighbor_current_cost:
                    continue
                # Else if the cost is smaller update the node with the new one and move it to the open list
                closed_dictionary[neighbor] = False
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_depth(current_node.get_depth())
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                open_dictionary[neighbor] = True
            else:
                # Else add the node to open list
                neighbor.set_g(neighbor_current_cost)
                neighbor.set_depth(current_node.get_depth())
                neighbor.set_parent(current_node)
                calculate_f_cost(maze, neighbor, end_node)
                heapq.heappush(open_heap, neighbor)
                open_dictionary[neighbor] = True

    return False
