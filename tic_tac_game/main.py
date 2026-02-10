import numpy as np

board = np.zeros((3,3),dtype=int)

def print_board(board):
    symbols = {0:"" , 1:'X' , -1:'O'}
    for r in range(3):
        row = "  | ".join(symbols[val] for val in board[r])
        print(" "+row)
        if r < 2 :
            print("---+---+---")


def check_winner(b):
    if 3 in np.sum(b,axis = 1 ) or 3 in np.sum(b,axis = 0):
        return 'X'
    if -3 in np.sum(b,axis = 1 ) or -3 in np.sum(b,axis = 0):
        return 'O'
    if -3 == np.trace(b) or -3 == np.trace(np.fliplr(b)):
        return 'O'
    if 3 == np.trace(b) or 3 == np.trace(np.fliplr(b)):
        return 'X'
    
    if not 0 in b:
        return 'DRAW'
    return None

current = 1

print("Welcome to tic tac tow game")

while True:
    if current == 1:
        player = 'X'
        
    else:
        player = 'O'

    try:
        row = int(input(player + " - Enter row (0,1,2)"))
        col = int(input(player + " - Enter column (0,1,2)"))
    except Exception as err:
        print("please enter valid number \n")
        continue
    
    if row < 0 or row > 2 or col < 0 or col > 2 :
        print("input col,row within range")
        continue
    
    if board[row,col] != 0:
        print("cell is already taken")
        continue
    
    board[row,col] = current
    print_board(board)

    result = check_winner(board)

    if result is not None:
        if result == "DRAW":
            print("U GOT A DRAW")
        else:
            print(result,"WINS")
        break

    current = -1 if current == 1 else 1

