# File: sweeper.py
# Description: Minesweeper in the command line.

# start with preset beginner size
ROWS = 9 ;
COLS = 9 ;

# initialize initial board with -1 (denoting nothing known)
known_board = [[1 for i in range(0, COLS)] for j in range(0, ROWS)]

# print_board() outputs the currently known state of the game board.
def print_board():
    output = "" ;

    for i in range(0, ROWS):
        line = "" ;

        for j in range(0, COLS):
            curr_space = known_board[i][j] ;

            # totally unknown
            if curr_space == -1:
                line += "-" ;
            # nothing
            elif curr_space == 0:
                line += " " ;
            # flag
            elif curr_space == 9:
                line += "!" ;
            else:
                line += str(curr_space) ;

            # padding between spaces
            line += " " ;
        
        # remove extra space and move to next line
        line.strip() ;
        output += line ;
        output += "\n" ;

    # remove extra newline
    output.strip() ;

    print(output) ;
# -- end print_board

print_board() ;
