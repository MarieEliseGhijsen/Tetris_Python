
_INTERVAL = 0.3
_BLOCK = "\u2588\u2588"

import keypresstest

import time
import sys

import random

def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(rows)] for i in range(columns)]
        
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
    
def run(): 
    get_grid_size()
    grid = build_clean_grid()