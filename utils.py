# utils.py
# Utility functions for the Flow Free game.

from copy import deepcopy
import glob
import os
import pdb
import random


def cutflow(board, direction, flow, anchors, start, row, col):
    '''Cut a flow when the user selects a cell (row, col) in the middle of the flow.
    Reduced flow should go from the start to the specified row and column.'''
    print("cutflow is unfinished method")
    # pdb.set_trace()
    # for i in range(len(board)):
    #     for j in range(len(board[i])):
    #         if board[i][j] == flow and [i, j] not in anchors[flow]:
    #             board[i][j] = 0

def get_matching_adjacent(board, row, col):
    '''Get adjacent cells on a board that contain the same value as the cell
    at a specified row and column. Adjacency does not include diagonals.'''
    # Extract grid size
    rows = len(board)
    cols = len(board[0])

    # Determine target value to match
    target = board[row][col]

    # Check valid adjacent cells
    matching = []
    if row > 0 and board[row-1][col] == target:  # cell above
        matching += [[row-1, col]]
    if row < rows - 1 and board[row+1][col] == target:  # cell below
        matching += [[row+1, col]]
    if col > 0 and board[row][col-1] == target:  # cell to the left
        matching += [[row, col-1]]
    if col < cols - 1 and board[row][col+1] == target:  # cell to the right
        matching += [[row, col+1]]
    
    return matching

def getboard(rows, cols):
    '''Get a board with a specified number of rows and columns.
    
    Currently, this method searches through a data directory to find potential
    boards that match the requested size (via filenames), then randomly selects
    a board from the list of matches.

    In the future, it may be desirable to randomly generate a board on the fly.

    TODO: Error checking for inputs that have no matches!
    '''
    # Find boards that match size request
    filenames = glob.glob(os.path.join('data', f'board_{rows}x{cols}*.txt'))
    
    # Randomly choose a file from the list
    file = random.choice(filenames)

    # Read data from file
    f = open(file, 'r')
    data = f.read()
    f.close()

    # Convert data to list of lists
    board = [[int(c) for c in i] for i in data.split('\n')]

    return board

def getanchors(solution):
    '''From a board solution, determine where the anchors of each flow are.
    Returns a copy of the board, where only anchors are visible (all other
    cells are set to 0). Also, returns a dictionary containing the (row, col)
    pairs for each endpoint of every flow.'''
    board = deepcopy(solution)
    n = getnumflows(solution)
    anchors = {item:[] for item in range(1, n+1)}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if len(get_matching_adjacent(solution, i, j)) > 1:
                board[i][j] = 0
            else:
                anchors[board[i][j]] += [[i, j]]
    
    return board, anchors

def getdirection(rows, cols):
    '''Initialize the direction of a flow for any cell in a grid of size (rows, cols).'''
    return [['' for j in range(cols)] for i in range(rows)]

def getnumflows(board):
    '''Given a board with nonzero values to represent unique flows,
    determine the number of flows on the board.'''
    return max([max(row) for row in board])

def resetflow(board, direction, flow, anchors):
    '''Erase the specified flow from the board, excluding the anchors.'''
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == flow:
                if [i, j] not in anchors[flow]:
                    board[i][j] = 0  # reset cell (excluding anchors)
                direction[i][j] = ''  # reset direction (including anchors)

def show(board):
    '''Utility function to display board in terminal.'''
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f'{board[i][j]:2d}', end=' ')
        print()

def traceflow(board, path, previous):
    '''Trace a flow on the board.'''
    pass

def update_from_click(board, row, col, anchors, flow_start, verbose=True):
    '''Update the board values based on the user clicking on the cell at
    a specified row and column.
    
    anchors -> dictionary of lists of anchors for each flow
    flow_start -> nonzero values represent current endpoint at which the flow starts'''
    if board[row][col] == 0:  # do nothing, the user clicked on an empty cell
        pass
    elif [row, col] in anchors[board[row][col]]:  # user clicked on an endpoint
        if verbose: print(f'You clicked on an endpoint for flow {board[row][col]}')
        flow = board[row][col]  # which flow are we dealing with
        resetflow(board, flow, anchors)
        flow_start[flow] = [row, col]
    elif board[row][col] != 0:  # user clicked on the middle of a flow
        if verbose: print(f'You clicked on the middle of flow {board[row][col]}')
        cutflow(board, row, col, flow_start)

def zeros(x):
    '''Utility function to copy a list (or list of lists) and replace all 
    elements with zero.'''
    y = deepcopy(x)
    for i in range(len(y)):
        if isinstance(y[i], list):
            for j in range(len(y[i])):
                y[i][j] = 0
        else:
            y[i] = 0

    return y