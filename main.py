from tkinter import *
from tkinter import filedialog

from AlgorithmType import *
from Maze import Maze
from Node import Node
import threading
import time

root = Tk()  # main window
root.title("Path Finding")
root.configure(background='#2b2b2b')
root.geometry("300x300")  # width X height
root.resizable(False, False)
max_time = 100


def import_file():  # a function to read a text file and analyze it
    global maze
    global max_time
    # file = filedialog.askopenfilename(initialdir="/", title="Select File",
    #                                   filetypes=(("Text", "*.txt"), ("All Files", "*.*")))
    file = "S:\\onedrive\\sync\\pythonAI\\matrices\\17.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\30.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\60.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\60-2.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\4_BIASTAR_30X30.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\test matrix 30.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\test matrix2 30.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\1000.txt"
    # file = "S:\\onedrive\\sync\\pythonAI\\matrices\\120a.txt"
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

    algo_type = AlgorithmType.ASTAR

    second_line = f.readline()
    size = int(second_line)

    # max_time = math.sqrt(size)

    third_line = f.readline()
    arr = [int(num) for num in third_line.split(',')]
    start = (arr[0], arr[1])

    fourth_line = f.readline()
    arr = [int(num) for num in fourth_line.split(',')]
    end = (arr[0], arr[1])

    matrix = [[int(num) for num in line.split(',')] for line in f if line.strip(' ') != ""]

    length = 0
    for row in matrix:
        for _ in row:
            length += 1

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

    average /= count

    print("average ", average)
    print("minimum ", minimum)

    maze = Maze(algotype=algo_type, size=size, start=start, end=end, matrix=matrix)

    f.close()
    make_grid(maze)
    set_neighbors(maze)
    start_button['state'] = NORMAL


def make_grid(maze):
    grid = []
    for i in range(maze.get_size()):
        grid.append([])
        for j in range(maze.get_size()):
            cost = maze.get_matrix()[i][j]
            node = Node(x=i, y=j, cost=cost)
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
    print('done')
    exit(0)


def timer(maze):    # todo: ida ids not working with timer
    start_time = time.time()
    while True:
        print('test')
        diff_time = time.time() - start_time
        if (not maze.running) and maze.found:
            return
        if diff_time > max_time and maze.running:
            maze.running = False
            print('not found')
            return

    # time.sleep(max_time)
    # if not maze.found:
    #     maze.running = False
    #     print('NOT FOUND')
    #     exit(0)


import_button = Button(root, text="Import Maze", command=import_file, bg='#3c3f41', fg='#a9b7c6', bd=0,
                       font=("JetBrains Mono", 18))
start_button = Button(root, text="Start Maze", command=start_maze, bg='#3c3f41', fg='#a9b7c6', bd=0, state=DISABLED,
                      font=("JetBrains Mono", 18))

import_button.grid(row=0, column=0, padx=70, pady=50)
start_button.grid(row=1, column=0, padx=70, pady=50)

root.mainloop()  # display window
