from tkinter import *
from tkinter import filedialog, Text
from AlgorithmType import *
from Point import Point
from Maze import Maze

root = Tk()  # main window
root.title("Path Finding")
root.configure(background='#2b2b2b')
root.geometry("500x400")  # width X height
root.resizable(False, False)
file = None
global maze




def import_file():
    global algo_type
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
    elif first_line == "IDS":
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

    maze = Maze(algoType=algo_type, size=size, start=start, end=end, matrix=matrix)

    f.close()


import_button = Button(root, text="Import Maze", command=import_file, bg='#3c3f41', fg='#a9b7c6', bd=0,
                       font=("JetBrains Mono", 18))
start_button = Button(root, text="Start Maze", bg='#3c3f41', fg='#a9b7c6', bd=0, state=DISABLED, font=("JetBrains Mono", 18))
# start_button['state'] = NORMAL    TO CHANGE BUTTON STATE
output_label = Label(root, text="Output:", bg='#2b2b2b', fg='#a9b7c6', font=("JetBrains Mono", 18))
output_text = Text(root, height=2, width=30)
# output_text.insert(END, "string")   ADD TEXT (THE RESULT)

import_button.grid(row=0, column=0, padx=180, pady=20)
start_button.grid(row=1, column=0, padx=180, pady=20)
output_label.grid(row=2, column=0, padx=180, pady=20)
output_text.grid(row=3, column=0, padx=10, pady=20)

root.mainloop()  # display window
