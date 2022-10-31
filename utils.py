# utils.py
# Utility functions for the game.

from copy import deepcopy
import pdb


def count_matching_adjacent(board, row, col):
    '''Count the number of adjacent cells on a board that contain the same
    value as the cell at a specified row and column.
    
    Adjacency does not include diagonals.'''
    # Extract grid size
    rows = len(board)
    cols = len(board[0])

    # Determine target value to match
    target = board[row][col]

    # Check valid adjacent cells
    matching = 0
    if row > 0 and board[row-1][col] == target:  # cell above
        matching += 1
    if row < rows - 1 and board[row+1][col] == target:  # cell below
        matching += 1
    if col > 0 and board[row][col-1] == target:  # cell to the left
        matching += 1
    if col < cols - 1 and board[row][col+1] == target:  # cell to the right
        matching += 1
    
    return matching
    

def getboard(rows, cols, n):
    '''Make a board with a specified number of rows, columns, and n flows.
    
    NOTES:
    1. Right now, I am hard-coding one board. In the future, this generation 
    should be pseudorandom perhaps?
    2. I am assuming the board parameters are reasonable, but may need some
    error-checking in the future.
    '''
    board = [[3, 1, 1, 1, 4],
            [3, 1, 5, 5, 4],
            [3, 1, 5, 4, 4],
            [3, 1, 4, 4, 2],
            [3, 3, 2, 2, 2]]

    return board


def getendpoints(solution):
    '''From a board solution, determine where the endpoints of each flow are.
    Returns a copy of the board, where only endpoints are visible (all other
    cells are set to 0).'''
    board = deepcopy(solution)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if count_matching_adjacent(solution, i, j) > 1:
                board[i][j] = 0
    
    return board


def show(board):
    '''Utility function to display board in terminal.'''
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f'{board[i][j]:2d}', end=' ')
        print()