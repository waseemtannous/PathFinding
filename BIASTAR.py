import time
import heapq

from Heuristics import *



def biAstar(maze):
    # maze.max_time = math.sqrt(maze.size)
    maze.max_time = 1000
    time_start = time.time()
    # Min heap for choosing the minimum cost every time.
    open_heap_start = []
    open_heap_end = []

    # Two hash tabels for each direction, open list (neighbors of the expanded node)
    # and close list (contains expanded nodes) ,O(1) time complixty for finding an item in the table
    open_dictionary_start = {}
    open_dictionary_end = {}

    closed_dictionary_start = {}
    closed_dictionary_end = {}

    # Getting the coordinates of start node and the goal node
    x1, y1 = maze.get_start()
    x2, y2 = maze.get_end()
    # Two grids, THE FIRST GRID WE RUN A star from the start
    # the second we run from the goal node
    grid = maze.get_grid()
    second_grid = maze.get_second_grid()
    # Getting start node and the goal node
    start_node = grid[x1][y1]
    end_node = second_grid[x2][y2]
    # For both of them We calculate the F value for the node
    # Push the start node to the min heap and put in the open list (open_dictionary)
    calculate_f_cost(maze, node=start_node, end=end_node)
    heapq.heappush(open_heap_start, start_node)
    open_dictionary_start[start_node] = True

    calculate_f_cost(maze, node=end_node, end=start_node)
    heapq.heappush(open_heap_end, end_node)
    open_dictionary_end[end_node] = True

    current_node_end = end_node

    came_from_start = {}
    came_from_end = {}

    previous_node_start = None
    previous_node_end = None
    # While the open list is not empty and we are not out of time continue
    while len(open_heap_start) != 0 and len(open_heap_end) and (time.time() - time_start <= maze.max_time):
        # We get the node with minimal cost
        current_node_start = heapq.heappop(open_heap_start)
        # Remove the node from the open list ,and add it to the close list
        open_dictionary_start[current_node_start] = False
        closed_dictionary_start[current_node_start] = True

        if previous_node_start:
            if not previous_node_start.is_neighbor(current_node_start):
                maze.update_cuttoff(previous_node_start.depth)

        previous_node_start = current_node_start
        # Getting the current node on the second grid
        temp1 = second_grid[current_node_start.get_x()][current_node_start.get_y()]
        # If the node is on close list from both sides ENTER HERE
        if closed_dictionary_end.get(temp1, False):
            temp1 = bidirectional_meeting_point(maze, temp1, open_heap_start, open_heap_end, open_dictionary_start,
                                                open_dictionary_end,
                                                closed_dictionary_start, closed_dictionary_end)
            maze.actual_time = time.time() - time_start
            # Make path
            recreate_bidirectional_path(maze, temp1, came_from_start, came_from_end)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node_start, end_node, open_dictionary_start, closed_dictionary_start,
                       came_from_start, open_heap_start)

        #   second one #######################
        # We get the node with minimal cost
        current_node_end = heapq.heappop(open_heap_end)
        # Remove the node from the open list ,and add it to the close list
        open_dictionary_end[current_node_end] = False
        closed_dictionary_end[current_node_end] = True

        if previous_node_end:
            if not previous_node_end.is_neighbor(current_node_end):
                maze.update_cuttoff(previous_node_end.depth)

        previous_node_end = current_node_end
        # Getting the current node on the second grid
        temp2 = grid[current_node_end.get_x()][current_node_end.get_y()]
        # If the node is on close list from both sides ENTER HERE
        if closed_dictionary_start.get(temp2, False):
            temp2 = bidirectional_meeting_point(maze, temp2, open_heap_start, open_heap_end, open_dictionary_start,
                                                open_dictionary_end,
                                                closed_dictionary_start, closed_dictionary_end)
            maze.actual_time = time.time() - time_start
            # Make path
            recreate_bidirectional_path(maze, temp2, came_from_start, came_from_end)
            return True
        maze.update_expanded_nodes()
        biAstar_helper(maze, current_node_end, start_node, open_dictionary_end, closed_dictionary_end, came_from_end,
                       open_heap_end)

    return False


def biAstar_helper(maze, current_node, end_node, open_dictionary, closed_dictionary, came_from, open_heap):
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
            closed_dictionary[neighbor] = False
            neighbor.set_g(neighbor_current_cost)
            neighbor.set_depth(current_node.get_depth())
            came_from[neighbor] = current_node
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
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            open_dictionary[neighbor] = True
        else:
            # Else add the node to open list
            neighbor.set_g(neighbor_current_cost)
            neighbor.set_depth(current_node.get_depth())
            came_from[neighbor] = current_node
            calculate_f_cost(maze, neighbor, end_node)
            heapq.heappush(open_heap, neighbor)
            open_dictionary[neighbor] = True
            closed_dictionary[neighbor] = False

# This function tries to improve meeting point
def bidirectional_meeting_point(maze, temp, open_heap_start, open_heap_end, open_dictionary_start, open_dictionary_end,
                                closed_dictionary_start, closed_dictionary_end):
    x, y = temp.get_x(), temp.get_y()
    min_sum_f = maze.get_grid()[x][y].get_f() + maze.get_second_grid()[x][y].get_f()
    min_node = temp

    while len(open_heap_start) != 0:
        current_node_start = heapq.heappop(open_heap_start)
        current_node_end = maze.get_second_grid()[current_node_start.get_x()][current_node_start.get_y()]
        if open_dictionary_end.get(current_node_end, False) or closed_dictionary_end.get(current_node_end, False):
            temp_min_f = current_node_start.get_f() + current_node_end.get_f()
            # Update the meeting point
            if temp_min_f < min_sum_f:
                min_sum_f = temp_min_f
                min_node = current_node_start

    while len(open_heap_end) != 0:
        current_node_end = heapq.heappop(open_heap_end)
        current_node_start = maze.get_grid()[current_node_end.get_x()][current_node_end.get_y()]
        if open_dictionary_start.get(current_node_start, False) or closed_dictionary_start.get(current_node_start, False):
            temp_min_f = current_node_end.get_f() + current_node_start.get_f()
            # Update the meeting point
            if temp_min_f < min_sum_f:
                min_sum_f = temp_min_f
                min_node = current_node_end
    return min_node


def recreate_bidirectional_path(maze, node, came_from_start, came_from_end):
    node_x = node.get_x()
    node_y = node.get_y()
    node = maze.get_second_grid()[node_x][node_y]
    maze.get_path().append(node)
    #Get the parents on the end side
    while came_from_end.get(node, False):
        node = came_from_end[node]
        maze.get_path().append(node)

    maze.get_path().reverse()
    node = maze.get_grid()[node_x][node_y]
    # Get the parents on the start side
    while node in came_from_start:
        node = came_from_start[node]
        maze.get_path().append(node)
