from tkinter import *
from tkinter import filedialog

from AlgorithmType import *
from Colors import *
from Maze import Maze
from Node import Node
import threading
import time
import sys
import os

root = Tk()  # main window
root.title("Path Finding")
root.configure(background='#2b2b2b')
root.geometry("300x300")  # width X height
root.resizable(False, False)
max_time = 0.000001


def import_file():  # a function to read a text file and analyze it
    global maze
    # file = filedialog.askopenfilename(initialdir="/", title="Select File",
    #                                   filetypes=(("Text", "*.txt"), ("All Files", "*.*")))
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\17.txt"
    file = "S:\\onedrive\\sync\\pythonAI\\matrices\\30.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\60.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\60-2.txt"
    f = open(file, 'r')

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

    second_line = f.readline()
    size = int(second_line)

    third_line = f.readline()
    arr = [int(num) for num in third_line.split(',')]
    start = (arr[0], arr[1])

    fourth_line = f.readline()
    arr = [int(num) for num in fourth_line.split(',')]
    end = (arr[0], arr[1])

    matrix = [[int(num) for num in line.split(',')] for line in f if line.strip(' ') != ""]

    average = 0
    minimum = matrix[0][0]
    count = 0

    for row in matrix:
        for num in row:
            if num != -1:
                count += 1
                average += num
                if num < minimum:
                    minimum = num

    average /= (count)

    print("average ", average)
    print("minimum ", minimum)

    maze = Maze(algotype=algo_type, size=size, start=start, end=end, matrix=matrix)

    f.close()
    make_grid(maze)
    set_neighbors(maze)
    start_button['state'] = NORMAL



def make_grid(maze):
    grid = []
    maze.set_square_size(800 // maze.get_size())
    for i in range(maze.get_size()):
        grid.append([])
        for j in range(maze.get_size()):
            cost = 0
            x1, y1 = maze.get_start()
            x2, y2 = maze.get_end()
            if i == x1 and j == y1:
                color = ORANGE
                cost = maze.get_matrix()[i][j]
            elif i == x2 and j == y2:
                color = TURQUOISE
                cost = maze.get_matrix()[i][j]
            elif maze.get_matrix()[i][j] == -1:
                color = BLACK
            else:
                color = WHITE
                cost = maze.get_matrix()[i][j]

            node = Node(x=i, y=j, color=color, cost=cost)
            grid[i].append(node)

    maze.set_grid(grid)


def set_neighbors(maze):
    grid = maze.get_grid()
    for row in grid:
        for node in row:
            node.set_neighbors(maze)



def start_maze():
    run_thread = threading.Thread(target=timer, args=[maze])
    run_thread.start()
    maze.run()
    exit(0)
    # run_thread.join()


def timer(maze):
    time.sleep(max_time)
    if not maze.found:
        maze.running = False
        print('NOT FOUND')
        exit(0)

import_button = Button(root, text="Import Maze", command=import_file, bg='#3c3f41', fg='#a9b7c6', bd=0,
                       font=("JetBrains Mono", 18))
start_button = Button(root, text="Start Maze", command=start_maze, bg='#3c3f41', fg='#a9b7c6', bd=0, state=DISABLED,
                      font=("JetBrains Mono", 18))

import_button.grid(row=0, column=0, padx=70, pady=50)
start_button.grid(row=1, column=0, padx=70, pady=50)

root.mainloop()  # display window
