# events.py
# Event methods for the Flow Free game.

import draw
from params import *
import pdb
import utils


def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()

def mouseclick(event, board, direction, anchors, start, verbose=False):
    '''Method for handling mouse clicks on the gui canvas.'''
    # Extract relevant parameters
    canvas = event.widget
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows

    # Determine which cell was clicked
    row = event.y // dy
    col = event.x // dx

    # Ignore clicks on empty cells
    if board[row][col] == 0:
        return 0

    # Otherwise, determine which flow was clicked
    flow = board[row][col]

    # Set canvas internal variables
    canvas.setvar("isclicked", True)
    canvas.setvar("current_position", [row, col])
    canvas.setvar("active_flow", flow)

    # There are two cases to consider
    if [row, col] in anchors[flow]:  # user clicked on an anchor
        if verbose: print(f'You clicked on an anchor for flow {flow}: ({row},{col})')
        utils.resetflow(board, direction, flow, anchors)
        start[flow] = [row, col]
        draw.flow(canvas, board, flow, start[flow], direction)

    else:  # the clicked clicked on the middle of an existing flow
        if verbose: print(f'You clicked on the middle of flow {flow}: ({row},{col})')
        utils.cutflow(board, direction, flow, anchors, start[flow], row, col)
        draw.flow(canvas, board, flow, start[flow], direction)

def mousedrag(event, board, direction, anchors, start, verbose=False):
    '''Method for handling when the user clicked and dragged the mouse.'''
    # Extract relevant parameters
    canvas = event.widget
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    x = event.x
    y = event.y

    # Ignore mouse motion if user did not click
    if not canvas.getvar("isclicked"):
        return 0

    # Ignore mouse mouse motion if cursor is outside window bounds
    if x <= 0 or y <= 0 or x >= wid or y >= hei:
        canvas.setvar("isclicked", False)
        canvas.setvar("current_position", None)
        canvas.setvar("active_flow", None)
        return 0

    # Determine location of cursor
    # if verbose: print(f'dragging inside window {x} {y}')
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows
    row = y // dy
    col = x // dx
    
    # Ignore motion if cell has not changed
    r0, c0 = canvas.getvar("current_position")
    if [row, col] == [r0, c0]:
        return 0

    # Ignore motion if move is not to empty cell or anchor
    flow = canvas.getvar("active_flow")
    if board[row][col] != 0 and [row, col] not in anchors[flow]:
        print(f'flow {flow}, ({row}, {col}), anchors: {anchors[flow]}')
        canvas.setvar("isclicked", False)
        canvas.setvar("current_position", None)
        canvas.setvar("active_flow", None)
        return 0

    # Ignore motion if flow loops back to starting anchor
    if [row, col] == start[flow]:
        canvas.setvar("isclicked", False)
        canvas.setvar("current_position", None)
        canvas.setvar("active_flow", None)
        return 0

    # Otherwise, set direction and update current position
    if row < r0:
        direction[r0][c0] = 'up'
    elif row > r0:
        direction[r0][c0] = 'down'
    elif col < c0:
        direction[r0][c0] = 'left'
    elif col > c0:
        direction[r0][c0] = 'right'
    canvas.setvar("current_position", [row, col])
    if verbose: print(f'You moved {direction[r0][c0]} from ({r0},{c0}) to ({row},{col})')

    # Update board at new location
    board[row][col] = flow
    draw.flow(canvas, board, flow, start[flow], direction)

    # Stop tracking if we reached an anchor
    if [row, col] in anchors[flow]:
        event.widget.setvar("isclicked", False)
        event.widget.setvar("current_position", None)
        event.widget.setvar("active_flow", None)
        return 0


def mouserelease(event, verbose=False):
    '''Method to handle when the mouse button is released.'''
    # if verbose: print("User released mouse")
    event.widget.setvar("isclicked", False)
    event.widget.setvar("current_position", None)
    event.widget.setvar("active_flow", None)