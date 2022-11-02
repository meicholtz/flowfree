# draw.py
# Helper functions for drawing Flow Free game elements on the GUI.

from params import *
import pdb
import tkinter as tk
import utils


def anchors(canvas, board):
    '''Draw circles for anchors on the input board.
    Color is identified by the integer value on the board.'''
    # Extract relevant parameters
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows
    rx = 0.3 * dx  # radius of circle
    ry = 0.3 * dy  # radius of circle

    # Find anchors on board
    for i in range(rows):
        for j in range(cols):
            # Skip if empty
            if board[i][j] == 0:
                continue
            
            # Otherwise, draw circle
            clr = COLORS['flows'][board[i][j]]
            x = (2 * j + 1) * dx // 2
            y = (2 * i + 1) * dy // 2
            canvas.create_oval(x-rx, y-ry, x+rx, y+ry, fill=clr, width=0)

def flow(canvas, board, flow, start, direction):
    '''Draw flow on the canvas based on start (row, col) and direction (array of moves).'''
    # Extract relevant parameters
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows

    # Delete current flow, if it exists
    tag = f'flow{flow}'  # f-string to label graphical components associated with the current flow
    canvas.delete(tag)

    # Draw new flow from the start
    r0, c0 = start  # unpack list
    whichdirection = direction[r0][c0]
    while whichdirection != "":
        # Compute next cell
        if whichdirection == 'up':
            r1 = r0 - 1
            c1 = c0
        elif whichdirection == 'down':
            r1 = r0 + 1
            c1 = c0
        elif whichdirection == 'left':
            r1 = r0
            c1 = c0 - 1
        elif whichdirection == 'right':
            r1 = r0
            c1 = c0 + 1
        else:
            print(f'ERROR: Unrecognized direction --> {whichdirection}')
        
        # Draw flow segment
        x0 = (2 * c0 + 1) * dx // 2
        y0 = (2 * r0 + 1) * dy // 2
        x1 = (2 * c1 + 1) * dx // 2
        y1 = (2 * r1 + 1) * dy // 2
        clr = COLORS['flows'][flow]
        canvas.create_line(x0, y0, x1, y1, fill=clr, width=24, tags=tag)
        canvas.create_oval(x1-11, y1-11, x1+11, y1+11, fill=clr, width=0, tags=tag)

        # Move to next cell
        r0, c0 = r1, c1
        whichdirection = direction[r0][c0]


def flows(canvas, board, verbose=False):
    '''Draw flows on the canvas based on current board state.'''
    # Extract relevant parameters
    wid = WIDTH  # canvas.winfo_width()
    hei = HEIGHT  # canvas.winfo_height()
    rows = len(board)
    cols = len(board[0])
    dx = wid // cols
    dy = hei // rows
    
    # Delete any current flows
    canvas.delete("flow")

    # Draw new flows
    if verbose: utils.show(board)
    for i in range(rows):
        for j in range(cols):
            # Skip if empty
            if board[i][j] == 0:
                continue
            
            # Otherwise, draw flow based on adjacent cells
            clr = COLORS['flows'][board[i][j]]
            x0 = (2 * j + 1) * dx // 2
            y0 = (2 * i + 1) * dy // 2
            matching = utils.get_matching_adjacent(board, i, j)
            for row, col in matching:
                x1 = (2 * col + 1) * dx // 2
                y1 = (2 * row + 1) * dy // 2
                canvas.create_line(x0, y0, x1, y1, fill=clr, width=24, tags="flow")
                canvas.create_oval(x1-11, y1-11, x1+11, y1+11, fill=clr, width=0, tags="flow")
    # pdb.set_trace()

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
        canvas.create_line(x0, y0, x1, y1, fill=COLORS['lines'], width=1.25)

    # Draw columns
    y0 = 0
    y1 = hei
    dx = wid // cols
    for i in range(1, cols):
        x0 = dx * i
        x1 = x0
        if verbose: print(f'Drawing vertical line from ({x0}, {y0}) to ({x1}, {y1})')
        canvas.create_line(x0, y0, x1, y1, fill=COLORS['lines'], width=1.25)

