from tkinter import *
from tkinter import filedialog

from AlgorithmType import *
from Maze import Maze
from Node import Node

# main UI
root = Tk()  # main window
root.title("Path Finding")
root.configure(background='#2b2b2b')
root.geometry("300x300")  # width X height
root.resizable(False, False)


def import_file():  # a function to read a text file and analyze it
    global maze
    # asks the user to input a valid file
    file = filedialog.askopenfilename(initialdir="/", title="Select File",
                                      filetypes=(("Text", "*.txt"), ("All Files", "*.*")))
    f = open(file, 'r')

    # determine which algorithm to run
    first_line = f.readline()
    if first_line == 'BIASTAR\n':
        algo_type = AlgorithmType.BIASTAR
    elif first_line == 'IDASTAR\n':
        algo_type = AlgorithmType.IDASTAR
    elif first_line == 'ASTAR\n':
        algo_type = AlgorithmType.ASTAR
    elif first_line == 'UCS\n':
        algo_type = AlgorithmType.UCS
    else:
        algo_type = AlgorithmType.IDS

    # matrix dimension
    second_line = f.readline()
    size = int(second_line)

    # start coordinates
    third_line = f.readline()
    arr = [int(num) for num in third_line.split(',')]
    start = (arr[0], arr[1])

    #   end coordinates
    fourth_line = f.readline()
    arr = [int(num) for num in fourth_line.split(',')]
    end = (arr[0], arr[1])

    # input the cost matrix
    matrix = [[int(num) for num in line.split(',')] for line in f if line.strip(' ') != ""]

    # save all relevant data in one object
    maze = Maze(algotype=algo_type, size=size, start=start, end=end, matrix=matrix)

    f.close()
    make_grid()
    set_neighbors()

    # allow the user to run the algorithm
    start_button['state'] = NORMAL


# this function makes nodes and arranges them in a grid
def make_grid():
    grid1 = []
    for i in range(maze.get_size()):
        grid1.append([])
        for j in range(maze.get_size()):
            cost = maze.get_matrix()[i][j]
            node = Node(x=i, y=j, cost=cost)
            grid1[i].append(node)

    maze.set_grid(grid1)

    # make the second grid to help us in biastar
    if maze.algotype == AlgorithmType.BIASTAR:
        grid2 = []
        for i in range(maze.get_size()):
            grid2.append([])
            for j in range(maze.get_size()):
                cost = maze.get_matrix()[i][j]
                node = Node(x=i, y=j, cost=cost)
                grid2[i].append(node)
        maze.set_second_grid(grid2)


# set the neighbors for every node
def set_neighbors():
    grid = maze.get_grid()
    for row in grid:
        for node in row:
            node.set_neighbors(maze, grid)
    if maze.algotype == AlgorithmType.BIASTAR:
        grid = maze.get_second_grid()
        for row in grid:
            for node in row:
                node.set_neighbors(maze, grid)


# starts the maze
def start_maze():
    maze.run()
    exit(0)


# here we add the UI buttons
import_button = Button(root, text="Import Maze", command=import_file, bg='#3c3f41', fg='#a9b7c6', bd=0,
                       font=("JetBrains Mono", 18))
start_button = Button(root, text="Start Maze", command=start_maze, bg='#3c3f41', fg='#a9b7c6', bd=0, state=DISABLED,
                      font=("JetBrains Mono", 18))

import_button.grid(row=0, column=0, padx=70, pady=50)
start_button.grid(row=1, column=0, padx=70, pady=50)

root.mainloop()  # display window
