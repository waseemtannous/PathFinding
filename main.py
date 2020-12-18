from tkinter import *
from tkinter import filedialog
from Point import Point
from Maze import *

root = Tk()  # main window
root.title("Path Finding")
root.configure(background='#2b2b2b')
root.geometry("300x300")  # width X height
root.resizable(False, False)
file = None
maze = Maze


def import_file():  # a function to read a text file and analyze it
    global maze
    file = filedialog.askopenfilename(initialdir="/", title="Select File",
                                      filetypes=(("Text", "*.txt"), ("All Files", "*.*")))
    f = open(file, 'r')

    first_line = f.readline()
    if first_line == "BIASTAR":
        algo_type = AlgorithmType.BIASTAR
    elif first_line == "IDASTAR":
        algo_type = AlgorithmType.IDASTAR
    elif first_line == "ASTAR":
        algo_type = AlgorithmType.ASTAR
    elif first_line == "UCS":
        algo_type = AlgorithmType.UCS
    else:
        algo_type = AlgorithmType.IDS

    second_line = f.readline()
    size = int(second_line)

    third_line = f.readline()
    arr = [int(num) for num in third_line.split(',')]
    start = Point(arr[0], arr[1])

    fourth_line = f.readline()
    arr = [int(num) for num in fourth_line.split(',')]
    end = Point(arr[0], arr[1])

    matrix = [[int(num) for num in line.split(',')] for line in f if line.strip() != ""]

    maze = Maze(algotype=algo_type, size=size, start=start, end=end, matrix=matrix)

    f.close()
    start_button['state'] = NORMAL

def start_maze():
    maze.run()


import_button = Button(root, text="Import Maze", command=import_file, bg='#3c3f41', fg='#a9b7c6', bd=0,
                       font=("JetBrains Mono", 18))
start_button = Button(root, text="Start Maze",command=start_maze, bg='#3c3f41', fg='#a9b7c6', bd=0, state=DISABLED,
                      font=("JetBrains Mono", 18))
# start_button['state'] = NORMAL    TO CHANGE BUTTON STATE

import_button.grid(row=0, column=0, padx=50, pady=20)
start_button.grid(row=1, column=0, padx=50, pady=20)

root.mainloop()  # display window
