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
parser.add_argument('-n', '--num', type=int,
                    help='number of flows to connect (defaults to smallest grid size)')
args = parser.parse_args()


def play(rows, cols, n):
    '''Play game with grid of size (rows, cols) and n flows.'''
    # Determine which board will be attempted
    solution = utils.getboard(rows, cols, n)  # which board are we trying to solve
    initial_board, endpoints = utils.getendpoints(solution)  # initial state is only endpoints
    current_board = deepcopy(initial_board)  # current state starts as initial state
    flow_start = {item:[] for item in endpoints.keys()}  # keep track of the start of each flow
    
    # Setup game interface
    gui = tk.Tk()
    gui.title("Flow Free")
    gui.iconbitmap("flowfree.ico")
    gui.resizable(False, False)  # make the window fixed

    canvas = tk.Canvas(gui, width=WIDTH, height=HEIGHT)
    canvas.configure(background=COLORS['background'])
    canvas.setvar("isclicked", False)  # flag for mouse clicks
    canvas.pack()

    # Draw stuff
    draw.grid(canvas, rows, cols)
    draw.endpoints(canvas, initial_board)

    # Add events
    gui.bind("<Escape>", events.endgame)
    gui.bind("<Button-1>", lambda evt: events.mouseclick(evt, canvas, current_board, endpoints, flow_start))
    gui.bind("<Motion>", lambda evt: events.mousedrag(evt, canvas, current_board))
    gui.bind("<ButtonRelease-1>", lambda evt: events.mouserelease(evt, canvas))

    # Run the game
    gui.mainloop()
    print('Thanks for playing!')

if __name__ == "__main__":
    rows, cols = [int(i) for i in args.size.split('x')]
    n = args.num if args.num is not None else min(rows, cols)
    play(rows, cols, n)