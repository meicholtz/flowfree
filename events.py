# events.py
# Event methods for the Flow Free game.

import draw
from params import *
import pdb
import utils


def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()

def mouseclick(event, board, anchors, flow_start, verbose=False):
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
        utils.resetflow(board, flow, anchors)
        flow_start[flow] = [row, col]
        draw.flows(canvas, board)

    else:  # the clicked clicked on the middle of an existing flow
        if verbose: print(f'You clicked on the middle of flow {flow}: ({row},{col})')
        utils.cutflow(board, row, col, flow_start)
        draw.flows(canvas, board)

def mousedrag(event, canvas, board):
    '''Method for handling when the user clicked and dragged the mouse.'''
    # Ignore mouse motion if user did not click
    if not canvas.getvar("isclicked"):
        return 0

    # Ignore mouse mouse motion if cursor is outside window bounds
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    x = event.x
    y = event.y
    if x <= 0 or y <= 0 or x >= wid or y >= hei:
        return 0

    print(f'dragging inside window {x} {y}')
    # Determine which cell was clicked
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows
    row = y // dy
    col = x // dx
    
    if [row, col] != canvas.getvar("current_position"):
        canvas.setvar("current_position", [row, col])  # update current active cell

        if board[row][col] == 0:
            board[row][col] = canvas.getvar("active_flow")
            draw.flows(canvas, board)
            print(x, y)

def mouserelease(event, verbose=False):
    '''Method to handle when the mouse button is released.'''
    if verbose: print("User released mouse")
    event.widget.setvar("isclicked", False)
    event.widget.setvar("current_position", None)
    event.widget.setvar("active_flow", None)