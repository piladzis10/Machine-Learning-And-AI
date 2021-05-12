"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    for row in board:
        for element in row:
            if element == "X":
                count_X +=1
            if element == "O":
                count_O +=1
    if count_X == count_O:
        return "X"
    else:
        return "O"



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.append((i,j))
    return actions

    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    bo = copy.deepcopy(board)
    
    if action in actions(board):
        bo[action[0]][action[1]] = player(board)    
    else: 
        raise Exception("Invalid move!")

    return bo


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal check
    for row in board:
        if row.count("X") == len(row):
            return "X"
        elif row.count("O") == len(row):
            return "O"

    # Vertical check
    for j in range(3):
        list = []
        for i in range(3):
            list.append(board[i][j])

        if list.count("X") == len(row):
            return "X"
        elif list.count("O") == len(row):
            return "O"
    
    # Diognal check
    for i in range(3):
        diognal_1 = []
        diognal_2 = []
        j_1 = i
        j_2 = 2 - i
        diognal_1.append(board[i][j_1])
        diognal_1.append(board[i][j_2])

        if diognal_1.count("X") == len(row) or diognal_2.count("X") == len(row):
            return "X"
        elif diognal_1.count("O") == len(row) or diognal_2.count("O") == len(row):
            return "O"

    return None
        
        

    

    
        




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0
i = 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None



    def max_value(board, step):
        v = 2

        act = actions(board)
        if len(act) == 1:
            bo = result(board, act[0])
            v = utility(bo)
        else:
            for action in act:
                bo = result(board, action)
                res = min_value(bo,step+1)
                v = max(v,res[0])
                step = res[1]
            if step == 0:
                return(action)
        step = 1
        return(v, step)

    def min_value(board, step):
        v = 2


        act = actions(board)
        if len(act) == 1:
            bo = result(board, act[0])
            v = utility(bo)
        else:
            for action in act:
                bo = result(board, action)
                res = max_value(bo,step + 1)
                v = min(v,res[0])
                step = res[1]
            if step == 0:
                return(action)

        step = 1
        return(v, step)


    if player(board) == "X":
       return max_value(board, 0)
    else:
        return min_value(board, 0)





    
