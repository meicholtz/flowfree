# utils.py
# Utility functions for the Flow Free game.

from copy import deepcopy
import pdb


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

def cutflow(board, row, col, flow_start):
    '''Cut a flow when the user selects a cell (row, col) in the middle of the flow.
    Determine how to cut it based on the known flow_start.'''
    print("cutflow: METHOD IS UNFINISHED")

def getboard(rows, cols):
    '''Make a board with a specified number of rows and columns.
    
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
    cells are set to 0). Also, returns a dictionary containing the (row, col)
    pairs for each endpoint of every flow.'''
    board = deepcopy(solution)
    n = getnumflows(solution)
    endpoints = {item:[] for item in range(1, n+1)}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if len(get_matching_adjacent(solution, i, j)) > 1:
                board[i][j] = 0
            else:
                endpoints[board[i][j]] += [[i, j]]
    
    return board, endpoints

def getnumflows(board):
    '''Given a board with nonzero values to represent unique flows,
    determine the number of flows on the board.'''
    return max([max(row) for row in board])
    
def resetflow(board, flow, endpoints):
    '''Erase the specified flow from the board, excluding the endpoints.'''
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == flow and [i, j] not in endpoints:
                board[i][j] = 0

def show(board):
    '''Utility function to display board in terminal.'''
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(f'{board[i][j]:2d}', end=' ')
        print()

def update_from_click(board, row, col, endpoints, flow_start, verbose=True):
    '''Update the board values based on the user clicking on the cell at
    a specified row and column.
    
    endpoints -> dictionary of lists of endpoints for each flow
    flow_start -> nonzero values represent current endpoint at which the flow starts'''
    if board[row][col] == 0:  # do nothing, the user clicked on an empty cell
        pass
    elif [row, col] in endpoints[board[row][col]]:  # user clicked on an endpoint
        if verbose: print(f'You clicked on an endpoint for flow {board[row][col]}')
        flow = board[row][col]  # which flow are we dealing with
        resetflow(board, flow, endpoints[flow])
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