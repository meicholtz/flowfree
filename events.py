# events.py
# Event methods for the Flow Free game.

import draw
from params import *
import pdb
import utils


def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()

def mouseclick(event, canvas, board, endpoints, flow_start, verbose=True):
    '''Method for handling mouse clicks on the gui canvas.'''
    # Set canvas internal variable
    if verbose: print("User clicked mouse")
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

    # Update the board values based on what was clicked
    utils.update_from_click(board, row, col, endpoints, flow_start)
    draw.flows(canvas, board)
    # pdb.set_trace()

def mousedrag(event, canvas, board):
    '''Method for handling when the user clicked and dragged the mouse.'''
    if canvas.getvar("isclicked"):
        print(event.x, event.y)

def mouserelease(event, canvas, verbose=True):
    '''Method to alert canvas that the mouse button was released.'''
    if verbose: print("User released mouse")
    canvas.setvar("isclicked", False)