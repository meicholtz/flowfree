# events.py
# Event methods for the Flow Free game.

from params import *
import pdb
import utils

def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()

def mouseclick(event, canvas, current_board, endpoints, flow_start, verbose=False):
    '''Method for handling mouse clicks on the gui canvas.'''
    # Extract relevant parameters
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(current_board)
    cols = len(current_board[0])
    dx = wid // cols
    dy = hei // rows

    # Determine which cell was clicked
    row = event.y // dy
    col = event.x // dx
    if verbose: print(f'You clicked on (row, col) = ({row}, {col})')

    # Update the board values based on what was clicked
    utils.update_from_click(current_board, row, col, endpoints, flow_start)
    # draw.flows(current_board, flow_start)
    # pdb.set_trace()