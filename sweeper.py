# File: sweeper.py
# Description: Minesweeper in the command line.

import random
import string
import math
import sys

# possible default sizes
SIZES = {"beginner": (9, 9, 10), "intermediate": (16, 16, 40),
            "expert": (16, 30, 99)}


num_revealed = 0

arg_err_message = ("Wrong arguments supplied. Arguments should be either " +
                    "\"beginner,\" \"intermediate,\" \"expert,\" or a custom" +
                    " size in the format \"[# rows] [# columns] [# mines]\"")

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
    col_letters = string.ascii_letters.swapcase()
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
        
        # move to next line
        output += line
        output += "\n"

    print(output)

    if not is_true_board:
        print("Mines: " + str(mines_left) + "\n")
# -- end print_board

# reveals neighbors of a square with 0 surrounding mines
def reveal_neighbors(row, col):
    news = set()
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if i >= 0 and i < ROWS and j >= 0 and j < COLS:
                if known_board[i][j] == -1:
                    global num_revealed
                    num_revealed += 1

                    # reveal again if a new 0 square is found
                    if true_board[i][j] == 0:
                        news.add((i, j))

                known_board[i][j] = true_board[i][j]

    for coords in news:
        reveal_neighbors(coords[0], coords[1])

# checks if the win condition (all non-mine squares revealed) is met
def check_for_victory():
    global num_revealed
    win_cond = num_revealed == ((ROWS * COLS) - MINES)

    return win_cond

# reveals this square and reveals its neighbors or detonates
def check_square(flag, row, col):
    known = known_board[row][col]
    true = true_board[row][col]
    game_not_over = True
    win = False

    # toggle flag
    if flag:
        global mines_left
        if known == -1:
            known_board[row][col] = 9
            mines_left -= 1
        elif known == 9:
            known_board[row][col] = -1
            mines_left += 1
    else:
        if known != -1:
            print("Cannot check this square.")
        else:
            if true == 9:
                print_board(True)
                print("You stepped on a mine! You lose.")
                game_not_over = False
            else:
                known_board[row][col] = true
                global num_revealed
                num_revealed += 1

                if true == 0:
                    reveal_neighbors(row, col)

    win = check_for_victory()

    return game_not_over, win

# checks that the flag, row, and col are acceptable values
def parse_input(user_input):
    flag = False
    row = -1
    col = -1

    num_valid = True
    flag_valid = True
    row_valid = False
    col_valid = False

    parts = user_input.split(" ")

    flag_part = ""
    row_part = ""
    col_part = ""

    # split inputs correctly
    if len(parts) == 3:
        flag_part = parts[0]
        row_part = parts[1]
        col_part = parts[2]
    elif len(parts) == 2:
        row_part = parts[0]
        col_part = parts[1]
    else:
        num_valid = False

    # check flag
    if flag_part and flag_part == "#":
        flag = True
        # flag_valid stays True

    if flag_part and flag_part != "#":
        # flag stays False
        flag_valid = False

    # check row
    if(row_part.isdigit()):
        # subtract one because the row display is 1-indexed
        row = int(row_part) - 1

        if row > -1 and row < ROWS:
            row_valid = True

    # check col
    if len(col_part) == 1:
        possible_cols = string.ascii_letters.swapcase()[:COLS]
        col = possible_cols.find(col_part)

        if col > -1 and col < COLS:
            col_valid = True

    valid = num_valid and flag_valid and row_valid and col_valid

    return valid, flag, row, col
# -- end parse_input

# verify that the custom command-line arguments are permissible
def verify_args(argv):
    if argv[1].isdigit() and argv[2].isdigit() and argv[3].isdigit():
        rows = int(argv[1])
        cols = int(argv[2])
        mines = int(argv[3])

        if rows < 1 or cols < 1:
            sys.exit("Cannot have zero or negative dimensions.")
        if cols > 52:
            sys.exit("Number of columns cannot be more than 52.")
        if mines > (rows * cols):
            sys.exit("Cannot have more mines than spaces on the board.")

        return True
    else:
        return False

# ----------------------------------------------------------------------

# should either be a single word or a set of three numbers
if len(sys.argv) != 2 and len(sys.argv) != 4:
    sys.exit(arg_err_message)

# one of the defaults
if len(sys.argv) == 2:
    if sys.argv[1].lower() in SIZES:
        size = SIZES[sys.argv[1].lower()]

        ROWS = size[0]
        COLS = size[1]
        MINES = size[2]
    else:
        sys.exit("Not a default size: beginner, intermediate, or expert.")
# custom size
elif len(sys.argv) == 4:
    if verify_args(sys.argv):
        ROWS = int(sys.argv[1])
        COLS = int(sys.argv[2])
        MINES = int(sys.argv[3])
    else:
        sys.exit(arg_err_message)

# initialize initial board with -1 (denoting nothing known)
# want to do board[row][col]
known_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

# initialize true board configuration with -1 as well
true_board = [[-1 for i in range(0, COLS)] for j in range(0, ROWS)]

mines_left = MINES

# ----------------------------------------------------------------------

game_active = True
win = False

set_mines()
count_mines()
print_board(False)

print("Input should be in the form of \"# (flag, opt) [number] [letter]\"")
print("\te.g. \"# 3 H\", \"# 14 b\", \"9 B\", \"7 Q\"")
print("Use \"exit\" to leave the game.")

while game_active:
    user_input = input("Enter coordinates of space to check: ")

    if user_input == "exit":
        game_active = False
    # TODO: remove this "special debugging command"
    elif user_input == "show true":
        print_board(True)
    else:
        valid, flag, row, col = parse_input(user_input)

        if valid:
            game_active, win = check_square(flag, row, col)
        else:
            print("\nInvalid input.\n")

        if win:
            game_active = False
            print_board(True)
            print("You win! Congratulations!")
        elif game_active:
            print_board(False)
