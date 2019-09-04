# File: sweeper.py
# Description: Minesweeper in the command line.

import random
import string
import math

# start with preset expert size
ROWS = 16
# at current, columns must be <= 52 due to character limitations...
COLS = 30
MINES = 99

# initialize initial board with -1 (denoting nothing known)
# want to do board[row][col]
known_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

# initialize true board configuration with -1 as well
true_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

# ----------------------------------------------------------------------

# choose squares to set mines on
def set_mines():
    squares = [-1 for i in range(0, ROWS * COLS)]

    for i in range(0, MINES):
        squares[i] = 9

    # pseudorandomly put these mines into new places
    random.shuffle(squares)

    # reformat into board shape
    for i in range(0, len(squares)):
        # floor divide to get how many rows down, what's left (mod) is col
        true_board[i // COLS][i % COLS] = squares[i]

# updates the values of the squares with the number of surrounding mines
def count_mines():
    for row in range(0, ROWS):
        for col in range(0, COLS):
            num_mines = 0

            if true_board[row][col] != 9:
                # scan 3x3 centered on current square
                for i in range(row - 1, row + 2):
                    for j in range(col - 1, col + 2):
                        # only count if square is on the board
                        if i >= 0 and i < ROWS and j >= 0 and j < COLS:
                            if true_board[i][j] == 9:
                                num_mines += 1

                true_board[row][col] = num_mines

# makes the column ids and delimiting line that are printed before the board
def make_col_ids():
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

# print_board() outputs the currently known state of the game board.
def print_board(is_true_board):
    output = ""

    output += make_col_ids()

    for i in range(0, ROWS):
        # add row index, incremented by one for 1-indexed addressing
        line = str(i + 1).rjust(int(math.log10(COLS) + 1))
        line += "|"

        for j in range(0, COLS):
            if(is_true_board):
                curr_space = true_board[i][j]
            else:
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
        output += line
        output += "\n"

    print(output)
# -- end print_board

# reveals neighbors of a square with 0 surrounding mines
def reveal_neighbors(row, col):
    news = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i >= 0 and i < ROWS and j >= 0 and j < COLS:
                # reveal again if a new 0 square is found
                if true_board[i][j] == 0 and known_board[i][j] == -1:
                    news.append((i, j))

                known_board[i][j] = true_board[i][j]

    for coords in news:
        reveal_neighbors(coords[0], coords[1])

# reveals this square and reveals its neighbors or detonates
def check_square(row, col, flag):
    known = known_board[row][col]
    true = true_board[row][col]
    valid_move = True

    # toggle flag
    if flag:
        if known == -1:
            known_board[row][col] = 9
        elif known == 9:
            known_board[row][col] = -1
    else:
        if known != -1:
            print("Already checked this square!")
        else:
            if true == 9:
                print_board(True)
                print("You stepped on a mine! You lose.")
                valid_move = False
            else:
                known_board[row][col] = true
                if true == 0:
                    reveal_neighbors(row, col)

    return valid_move

# checks that the input is a valid row value: an integer between 1 and ROWS
def validate_row(val):
    output = False

    if(val.isdigit()):
        if int(val) > 0 and int(val) <= ROWS:
            output = True

    return output

# handle user input by rejecting or checking the indicated square
def parse_input(user_input):
    row = -1
    col = -1
    flag = False

    parts = user_input.split(" ")

    # TODO: check input validity

    # subtract one because the row display is 1-indexed
    row = int(parts[0]) - 1

    col_id = ord(parts[1])

    # A-Z, 65-90
    if col_id < 97:
        col = col_id - 65
    # a-z, 97-122
    else:
        col = col_id - 71

    if len(parts) == 3:
        if parts[2] == "F":
            flag = True

    return row, col, flag

# ----------------------------------------------------------------------

game_active = True

set_mines()
count_mines()
print_board(False)

print("Input should be in the form of \"[number] [letter] F (flag, opt.)\"")
print("\te.g. \"3 H F\", \"14 b F\", \"9 B\", \"7 Q\"")
print("Use \"exit\" to leave the game.")

while game_active:
    user_input = input("Enter coordinates of space to check: ")

    if user_input == "exit":
        game_active = False
    # TODO: remove this "special debugging command"
    elif user_input == "show true":
        print_board(True)
    else:
        row, col, flag = parse_input(user_input)
        game_active = check_square(row, col, flag)
        print_board(False)

