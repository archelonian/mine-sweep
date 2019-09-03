# File: sweeper.py
# Description: Minesweeper in the command line.

import random

# start with preset beginner size
ROWS = 9
COLS = 9
MINES = 10

# initialize initial board with -1 (denoting nothing known)
known_board = [[1 for i in range(0, COLS)] for j in range(0, ROWS)]

# initialize true board configuration as -1 as well
true_board = [[1 for i in range(0, COLS)] for j in range(0, ROWS)]

# choose spaces to set mines on
def set_mines():
    spaces = [0 for i in range(0, ROWS * COLS)]

    for i in range(0, MINES):
        spaces[i] = 1

    # pseudorandomly put these mines into new places
    random.shuffle(spaces)

    # reformat into board shape
    for i in range(0, len(spaces)):
        # true_board[row][col]
        true_board[i // ROWS][i % COLS] = spaces[i]

# print_board() outputs the currently known state of the game board.
def print_board():
    output = ""

    for i in range(0, ROWS):
        line = ""

        for j in range(0, COLS):
            curr_space = known_board[i][j]

            # totally unknown
            if curr_space == -1:
                line += "-"
            # nothing
            elif curr_space == 0:
                line += " "
            # flag
            elif curr_space == 9:
                line += "!"
            else:
                line += str(curr_space)

            # padding between spaces
            line += " "
        
        # remove extra space and move to next line
        line.strip()
        output += line
        output += "\n"

    # remove extra newline
    output.strip()
    print(output)
# -- end print_board

set_mines()
print_board()
