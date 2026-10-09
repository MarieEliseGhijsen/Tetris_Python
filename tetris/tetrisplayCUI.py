
_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"

import keypresstest

import time
import sys

import random

def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")    # ANSI escape which clears the current terminal screen.
    sys.stdout.flush()

def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]

def drop_block(grid, column_number):
    """Given a column number, update the tetris grid to add a block to that column.
    Return the updated grid to the caller."""
    try:
        n = grid[column_number].index(_BLOCK)
        n = n - 1
    except:
        n = -1
    grid[column_number][n] = _BLOCK
    return grid

def display_grid(grid):
    """Display the current state of the tetris grid "vertically" up the screen. Remember: by default,
    the grid dispays across the screen, row-wise (which, usually, isn't what we want here)."""
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            print(grid[c][r], "|", sep="", end="")
        print()

def show_dropping_block(grid, column_number):
    """Given a grid and a column to drop into, simulate a visual drop of a box."""
    if check_space(grid, column_number):
        for row in range(_ROWS):
            if keypresstest.key_pressed == "Key.left" and column_number > 0 and grid[column_number - 1][row] != "\u2588\u2588":
                column_number -= 1
                #print("Left")
            if keypresstest.key_pressed == "Key.right"and column_number < _COLUMNS - 1 and grid[column_number + 1][row] != "\u2588\u2588":
                column_number += 1
                #print("Right")
                
            keypresstest.key_pressed = ""
            grid[column_number][row] = _BLOCK
            display_grid(grid)

            time.sleep(_INTERVAL)
            clear_the_terminal()
        
            grid[column_number][row] = _BLANK

            if row + 1 < _ROWS:
                if grid[column_number][row + 1] == _BLOCK: break
        
            grid[column_number][row] = _BLANK
            display_grid(grid)
            #time.sleep(_INTERVAL)
            clear_the_terminal()
        drop_block(grid, column_number)

    return column_number

#    for row in range(_ROWS):
#        grid[column_number][row] = _BLOCK
#        display_grid(grid)
#        time.sleep(_INTERVAL)
#        clear_the_terminal()
#        
#        grid[column_number][row] = _BLANK
#        
#        if row + 1 < _ROWS:
#            if grid[column_number][row + 1] == _BLOCK: break
#        
#        grid[column_number][row] = _BLANK
#        display_grid(grid)
#        #time.sleep(_INTERVAL)
#        clear_the_terminal()
#    drop_block(grid, column_number)
    
def check_space(grid, column_number):
    if grid[column_number][0] != "\u2588\u2588":
        return True
    return False
    
def run():
    g = build_clean_grid()
    c = 0
    
    for row in range(0, 70):
        r = random.randint(0, _COLUMNS - 1)
        if check_space(g, r):
            show_dropping_block(g, r)
        else:
            for column in range(_COLUMNS):
                if g[column][0] == "\u2588\u2588":
                    c = c + 1
                if c >= _COLUMNS:
                    break
                else:
                    c = 0
            
    clear_the_terminal()
    print("GAME END")