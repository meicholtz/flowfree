# flowfree.py
# Play Flow Free in Python!

import argparse
import draw
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
    solution = utils.getboard(rows, cols, n)
    initial_board = utils.getendpoints(solution)

    # Setup game interface
    gui = tk.Tk()
    gui.title("Flow Free")
    gui.iconbitmap("flowfree.ico")
    gui.resizable(False, False)  # make the window fixed

    canvas = tk.Canvas(gui, width=WIDTH, height=HEIGHT)
    canvas.configure(background=COLORS['background'])
    canvas.pack()

    # Draw stuff
    draw.grid(canvas, rows, cols)

    # Add events
    gui.bind("<Escape>", endgame)

    # Run the game
    gui.mainloop()
    print('Thanks for playing!')


def endgame(event):
    '''Method to quit the game.'''
    event.widget.destroy()


def guisetup():
    '''Setup root tkinter window.'''
    root = tk.Tk()
    root.title("Flow Free")
    root.iconbitmap("flowfree.ico")
    x = (root.winfo_screenwidth() - WIDTH) // 2
    y = (root.winfo_screenheight() - HEIGHT) // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")  # adjust the size of the window
    root.resizable(False, False)  # make the window fixed

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, background=COLORS['bg'], borderwidth=0)
    canvas.setvar('stillplaying', True)
    canvas.pack()

    return root, canvas


if __name__ == "__main__":
    rows, cols = [int(i) for i in args.size.split('x')]
    n = args.num if args.num is not None else min(rows, cols)
    play(rows, cols, n)