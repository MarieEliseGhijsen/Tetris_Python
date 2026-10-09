
_INTERVAL = 0.3
_BLOCK = "\u2588\u2588"

import keypresstest

import time
import sys

import random

def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(rows)] for i in range(columns)]
    
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
    
def check_space(grid, column_number):
    if grid[column_number][0] != _BLOCK:
        return True
    return False
    
def get_grid_size():
    global rows
    global columns
    
    while True:
        rows = int(input("enter a ROWS number between 3 and 10 : "))
        if rows >= 3 and rows <= 10 :
            break
   
    while True:
        columns = int(input("enter a COLUMNS number between 3 and 10 : "))
        if columns >= 3 and columns <= 10 :
            break
    
    #print("enter a number between 2 and 10 : ")
    #buffer = ""
    
    #while True:
    #    if keypresstest.key_pressed is not None:
    #        if keypresstest.key_pressed == "Key.enter": #wait till enetr key
    #            if buffer.isdigit(): #checks if all characters in string are digits [0-9]
                   
    #                print("in digit if")
                   
    #                number = int(buffer)
    #                if number >= 2 and number <= 10:
    #                    
    #                    print("returning number")
    #                    
    #                    keypresstest.key_pressed = None
    #                    return number
    #                else:
    #                    print("that is not a number between 2 and 10.")
    #            else:
    #                print("that is not a number.")
    #                keypresstest.key_pressed = None
    #            buffer = ""
                
    #        if keypresstest.key_pressed == "Key.up":
    #            keypresstest.key_pressed = None
    #            break
                
            #keypresstest.key_pressed = None
            
def display_grid(grid):
    """Display the current state of the tetris grid "vertically" up the screen. Remember: by default,
    the grid dispays across the screen, row-wise (which, usually, isn't what we want here)."""    
    for r in range(rows):
        print("|", sep="", end="")
        for c in range(columns):
            print(grid[c][r], "|", sep="", end="")
        print()
    
def run(): 
    get_grid_size()
    grid = build_clean_grid()
    
    display_grid(grid)