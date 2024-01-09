board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]


# Print board with 3x3 boards
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("------------------")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|", end="")
            if j == (len(board[0])-1):
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ",  end="")

# Find empty cell/zero in sudoku board


def find_zero(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return ([i, j])
    return None

# is Valid placement inboard?


def is_valid(board, row, col, value):
    # if Row has already value
    for i in board[row]:
        if i == value:
            return False
    # if Col has already value
    for i in range(1):
        for j in range(len(board[0])):
            if board[j][col] == value:
                return False

    # Check 3x3 matrix where element falls

          # if not, check if the input value already exites in 3x3 grid
    x = (row//3)*3
    y = (col//3)*3

    for i in range(3):
        for j in range(3):
            if board[i+x][j+y] == value:
                return False

    return True

 # Base Case


def solve(board):
    # Base Case, If there is no Zero return the board
    zPoint = find_zero(board)
    if zPoint == None:
        return print_board(board)
    # Recursive Cases
    x = zPoint[0]
    y = zPoint[1]
    for i in range(1, 10):
        if is_valid(board, x, y, i):
            board[x][y] = i
            solve(board)
            # Reset the value if the number was wrong
            board[x][y] = 0
    # Result if there is no solution
    return None


solve(board)
