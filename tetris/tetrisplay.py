
_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"

import time
from IPython.display import clear_output

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

    for row in range(_ROWS):
        grid[column_number][row] = _BLOCK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_output(wait=True)
        grid[column_number][row] = _BLANK
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_output(wait=True)