# draw.py
# Helper functions for drawing game elements on the GUI.

from params import *
import pdb
import tkinter as tk


def grid(canvas, rows, cols, verbose=False):
    '''Draw lines based on requested grid size (rows, cols).'''
    # Extract size of canvas
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()

    # Draw rows
    x0 = 0
    x1 = wid
    dy = hei // rows
    for i in range(1, rows):
        y0 = dy * i
        y1 = y0
        if verbose: print(f'Drawing horizontal line from ({x0}, {y0}) to ({x1}, {y1})')
        line = canvas.create_line(x0, y0, x1, y1, fill=COLORS['lines'], width=1)

    # Draw columns
    y0 = 0
    y1 = hei
    dx = wid // cols
    for i in range(1, cols):
        x0 = dx * i
        x1 = x0
        if verbose: print(f'Drawing vertical line from ({x0}, {y0}) to ({x1}, {y1})')
        line = canvas.create_line(x0, y0, x1, y1, fill=COLORS['lines'], width=1)

