# flowfree.py
# Play Flow Free in Python!

import argparse
from copy import deepcopy
import draw
import events
from params import *
import pdb
import tkinter as tk
import utils

parser = argparse.ArgumentParser(description="Play Flow Free in Python")
parser.add_argument('-sz', '--size', type=str,
                    help='size of the grid, given as #x# string (defaults to 5x5)',
                    default='5x5')
# parser.add_argument('-n', '--num', type=int,
#                     help='number of flows to connect (defaults to smallest grid size)')
args = parser.parse_args()


def play(rows, cols):
    '''Play game with grid of size (rows, cols) and n flows.'''
    # Determine which board will be attempted
    solution = utils.getboard(rows, cols)  # which board are we trying to solve
    initial_board, anchors = utils.getanchors(solution)  # initial state is only anchors
    current_board = deepcopy(initial_board)  # current state starts as initial state
    current_direction = utils.getdirection(rows, cols)  # initial direction of flows for each cell  
    flow_start = {item:[] for item in anchors.keys()}  # keep track of the start of each flow
    
    # Setup game interface
    gui = tk.Tk()
    gui.title("Flow Free")
    gui.iconbitmap("circle.ico")
    gui.resizable(False, False)  # make the window fixed

    canvas = tk.Canvas(gui, width=WIDTH, height=HEIGHT)
    canvas.configure(background=COLORS['background'])
    canvas.pack()

    # Add data to canvas
    canvas.setvar("unsolved", True)  # flag to determine if game is still going
    canvas.setvar("isclicked", False)  # flag for mouse clicks
    canvas.setvar("current_position", None)  # store location (row, col) of mouse click-and-drag
    canvas.setvar("active_flow", None)  # keep track of flow being edited
    
    # Draw stuff
    draw.grid(canvas, rows, cols)
    draw.anchors(canvas, initial_board)

    # Add events
    gui.bind("<Escape>", events.endgame)
    gui.bind("<Button-1>", lambda evt: events.mouseclick(evt, current_board, current_direction, anchors, flow_start, verbose=VERBOSE))
    gui.bind("<Motion>", lambda evt: events.mousedrag(evt, current_board, current_direction, anchors, flow_start, verbose=VERBOSE))
    gui.bind("<ButtonRelease-1>", lambda evt: events.mouserelease(evt, verbose=VERBOSE))

    # Run the game
    gui.mainloop()
    print('Thanks for playing!')

if __name__ == "__main__":
    rows, cols = [int(i) for i in args.size.split('x')]
    # n = args.num if args.num is not None else min(rows, cols)
    play(rows, cols)