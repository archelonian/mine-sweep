# File: sweeper.py
# Description: Minesweeper in the command line.

import random
import string
import math

# start with preset beginner size
ROWS = 16
# at current, columns <= 52 due to character limitations...
COLS = 30
MINES = 99

# initialize initial board with -1 (denoting nothing known)
# want to do board[row][col]
known_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

# initialize true board configuration as -1 as well
true_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

# choose spaces to set mines on
def set_mines():
    spaces = [0 for i in range(0, ROWS * COLS)]

    for i in range(0, MINES):
        spaces[i] = 1

    # pseudorandomly put these mines into new places
    random.shuffle(spaces)

    # reformat into board shape
    for i in range(0, len(spaces)):
        # floor divide to get how many rows down, what's left (mod) is col
        true_board[i // COLS][i % COLS] = spaces[i]

# print_board() outputs the currently known state of the game board.
def print_board():
    output = ""

    output += make_col_ids()

    for i in range(0, ROWS):
        # add row index, incremented by one for 1-indexed addressing
        line = str(i + 1).rjust(int(math.log10(COLS) + 1))
        line += "|"

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
                line += "#"
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

# makes the column ids and delimiting line that are printed before the board
def make_col_ids():
    # total width of column indices
    # number of digits + | + (number of columns * 2) - 1 from last space
    width = (int(math.log10(COLS)) + 1) + 1 + (2 * COLS) - 1

    # use A-Z then a-z
    col_letters = string.ascii_uppercase + string.ascii_lowercase
    col_letters = col_letters[:COLS]

    # separate letters with spaces
    col_spaces = " " * COLS
    col_ids = "".join(c1 + c2 for c1, c2 in zip(col_letters, col_spaces))

    # strip trailing space to line up properly with final column
    output = col_ids.strip().rjust(width) + "\n"

    # delimiting line of all -----------
    # subtract one to correspond with trailing space stripped above
    output += ("-" * (len(col_ids) - 1)).rjust(width)

    output += "\n"

    return output
# -- end make_col_ids

set_mines()
print_board()
