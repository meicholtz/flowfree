# events.py
# Event methods for the Flow Free game.

import draw
from params import *
import pdb
import utils


def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()

def mouseclick(event, canvas, board, endpoints, flow_start, verbose=False):
    '''Method for handling mouse clicks on the gui canvas.'''
    # Set canvas internal variable
    canvas.setvar("isclicked", True)

    # Extract relevant parameters
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows

    # Determine which cell was clicked
    row = event.y // dy
    col = event.x // dx
    if verbose: print(f'You clicked on (row, col) = ({row}, {col})')
    canvas.setvar("current_position", [row, col])
    canvas.setvar("active_flow", board[row][col])

    # Update the board values based on what was clicked
    utils.update_from_click(board, row, col, endpoints, flow_start)
    draw.flows(canvas, board)
    # pdb.set_trace()

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

def mouserelease(event, canvas, verbose=True):
    '''Method to alert canvas that the mouse button was released.'''
    if verbose: print("User released mouse")
    canvas.setvar("isclicked", False)
    canvas.setvar("current_position", None)
    canvas.setvar("active_flow", None)