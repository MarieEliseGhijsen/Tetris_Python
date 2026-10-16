from time import monotonic

import csv
import random

from pathlib import Path

from rich.text import Text

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Static

DEFAULT_COLUMNS = 5
DEFAULT_ROWS = 10

MIN_SIZE = 3
MAX_SIZE = 10

BLOCK = "\u2588\u2588"
BLANK = "  "

COLOURS = [ "red", "blue", "yellow", "green", "black", "orange", ]

RESULTS_FILE = "scores.csv"

game = {}

def build_clean_grid(rows, columns):
    """Reset the tetris grid to empty."""
    return [[None for column in range(columns)] for row in range(rows)]

def get_grid_size(app):
    name = app.query_one("#player", Input).value.strip()

    try:
        rows = int(app.query_one("#rows", Input).value)
        columns = int(app.query_one("#columns", Input).value)
    except ValueError:
        app.query_one("#message", Static).update("Rows and columns must be whole numbers.")
        return False

    if not name:
        app.query_one("#message", Static).update("Please enter your name.")
        return False

    if not MIN_SIZE <= rows <= MAX_SIZE:
        app.query_one("#message", Static).update("Rows must be between 3 and 10.")
        return False

    if not MIN_SIZE <= columns <= MAX_SIZE:
        app.query_one("#message", Static).update("Columns must be between 3 and 10.")
        return False

    game["name"] = name
    game["rows"] = rows
    game["columns"] = columns
    game["grid"] = build_clean_grid(rows, columns)

    return True

def drop_block(grid, row, column, colour):
    """Given a column number, update the tetris grid to add a block to that column.
    Return the updated grid to the caller."""
    grid[row][column] = colour

def check_space(grid, row, column):
    return grid[row][column] is None

def clear_full_rows(grid):
    '''removes all full rows and moves remaining rows down'''
    columns = len(grid[0])
    rows = len(grid)

    remaining_rows = [row for row in grid if not all(cell is not None for cell in row)]
    cleared = rows - len(remaining_rows)

    #add empty rows at top to keep grid size
    empty_rows = [[None for column in range(columns)] for row in range(cleared)]
    grid[:] = empty_rows + remaining_rows

    return cleared

def spawn_block(app):
    """make new block in random column"""
    grid = game["grid"]
    columns = game["columns"]

    available_columns = [column for column in range(columns) if check_space(grid, 0, column)]

    if not available_columns:
        finish_game(app)
        return

    game["active_row"] = 0
    game["active_column"] = random.choice(available_columns)
    game["active_colour"] = random.choice(COLOURS)

def refresh_board(app):
    """display grid and falling block"""
    grid = game["grid"]
    board = Text()

    for row in range(game["rows"]):
        board.append("|")

        for column in range(game["columns"]):
            colour = grid[row][column]

            #display falling block before its in place
            if (row == game.get("active_row") and column == game.get("active_column") and game.get("active_colour") is not None):
                colour = game["active_colour"]

            if colour is None:
                board.append(BLANK, style="dim")
            elif colour == "black":
                board.append(BLOCK, style="black on white")
            else:
                board.append(BLOCK, style=colour)

            board.append("|")

        board.append("\n")

    app.query_one("#board", Static).update(board)

def calculate_score(blocks, elapsed, rows, columns):
    """Calculate final score"""
    return (blocks * 100 + int(elapsed) * 2 + rows * columns * 5)

def save_result(name, elapsed, blocks, rows, columns, score):
    """save result in CSV file"""
    filename = Path(RESULTS_FILE)
    file_exists = filename.exists() and filename.stat().st_size > 0

    with filename.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Time_seconds", "Blocks_processed","Rows", "Columns", "Score"])
            
        writer.writerow([name, f"{elapsed:.2f}", blocks, rows, columns, score])

def update_clock(app):
    """Update displayed time while the game is running"""
    if not game.get("started") or game.get("paused"):
        return

    game["elapsed"] = monotonic() - game["start_time"]
    minutes, seconds = divmod(int(game["elapsed"]), 60)

    app.query_one("#timer", Static).update(f"Time: {minutes:02d}:{seconds:02d} | "f"Blocks: {game['blocks']} | "f"Grid: {game['columns']} x {game['rows']}")

def start_game(app):
    """Initialise game and start timer"""
    if game.get("started"):
        return

    if not get_grid_size(app):
        return

    game["blocks"] = 0
    game["elapsed"] = 0.0
    game["start_time"] = monotonic()
    game["started"] = True
    game["paused"] = False
    game["over"] = False

    game["active_row"] = None
    game["active_column"] = None
    game["active_colour"] = None

    app.query_one("#setup").display = False
    app.query_one("#game").display = True

    app.game_timer.resume()
    app.clock_timer.resume()

    spawn_block(app)
    refresh_board(app)
    update_clock(app)

def game_tick(app):
    """move active block down row"""
    if not game.get("started") or game.get("paused"):
        return
        
    if game.get("active_row") is None:
        spawn_block(app)

    if not game.get("started"):
        return

    grid = game["grid"]
    row = game["active_row"]
    column = game["active_column"]

    next_row = row + 1

    #check whether falling block can fall more
    if (next_row >= game["rows"] or not check_space(grid, next_row, column)):
        #the block is landed
        drop_block(grid, row, column, game["active_colour"],)
        game["blocks"] += 1
        clear_full_rows(grid)

        game["active_row"] = None
        game["active_column"] = None
        game["active_colour"] = None

        spawn_block(app)

    else:
        game["active_row"] = next_row

    refresh_board(app)
    update_clock(app)

def pause_game(app):
    """pause the game and timer"""
    if game.get("started") and not game.get("paused"):
        game["elapsed"] = monotonic() - game["start_time"]
        game["paused"] = True

        app.game_timer.pause()
        app.clock_timer.pause()

        app.query_one("#status", Static).update("Game paused.")

def resume_game(app):
    """resume game"""
    if game.get("started") and game.get("paused"):
        game["start_time"] = monotonic() - game["elapsed"]
        game["paused"] = False

        app.game_timer.resume()
        app.clock_timer.resume()

        app.query_one("#status", Static).update("Use the LEFT and RIGHT arrow keys to move.")

def finish_game(app):
    """stop game - calculate score + save"""
    if not game.get("started") or game.get("over"):
        return

    game["elapsed"] = monotonic() - game["start_time"]
    game["started"] = False
    game["paused"] = False
    game["over"] = True

    app.game_timer.pause()
    app.clock_timer.pause()

    score = calculate_score(game["blocks"], game["elapsed"], game["rows"], game["columns"],)
    save_result(game["name"], game["elapsed"], game["blocks"], game["rows"], game["columns"], score,)

    app.query_one("#timer", Static).update(f"Final time: {game['elapsed']:.1f} seconds")
    app.query_one("#status", Static).update(f"GAME OVER! {game['name']} | "f"Score: {score} | "f"Blocks: {game['blocks']}")

    refresh_board(app)

class TetrisApp(App):
    """Small Textual interface; game logic is in functions."""

    CSS = """
    Screen {align: center top;}
    
    #setup {width: 60; height: auto; border: round $primary; padding: 1 2; margin: 1;}
    #game {width: auto; height: auto; align: center top; padding: 1;}
    #board {width: auto; height: auto; border: round $primary; padding: 1; margin: 1; text-align: center;}
    #timer, #status {width: auto; height: auto; padding: 1; text-align: center;}

    Input {margin: 1 0;}

    #controls {width: auto; height: auto; align: center middle;}

    Button {margin: 1;}"""

    BINDINGS = [("left", "move_left", "Move left"), ("right", "move_right", "Move right"),("q", "quit_game", "Quit"),]

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="setup"):
            yield Static("TETRIS - GAME SETUP")
            yield Static("Player name:")
            yield Input(placeholder="Enter your name", id="player")

            yield Static("Number of rows (3-10, default 10):")
            yield Input(value=str(DEFAULT_ROWS), id="rows")

            yield Static("Number of columns (3-10, default 5):")
            yield Input(value=str(DEFAULT_COLUMNS), id="columns")

            yield Button("Start Game", id="start", variant="success")
            yield Static("", id="message")

        with Vertical(id="game"):
            yield Static("", id="timer")
            yield Static("", id="board")
            yield Static("Use the LEFT and RIGHT arrow keys to move.", id="status",)

            with Horizontal(id="controls"):
                yield Button("Pause", id="pause")
                yield Button("Resume", id="resume")
                yield Button("End Game", id="end", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#game").display = False
        self.game_timer = self.set_interval(0.3, lambda: game_tick(self), pause=True)
        self.clock_timer = self.set_interval(0.1, lambda: update_clock(self), pause=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            start_game(self)
        elif event.button.id == "pause":
            pause_game(self)
        elif event.button.id == "resume":
            resume_game(self)
        elif event.button.id == "end":
            finish_game(self)

    def action_move_left(self) -> None:
        """move the falling block one column to the left"""
        if (not game.get("started") or game.get("paused") or game.get("active_row") is None):
            return

        row = game["active_row"]
        column = game["active_column"] - 1

        if column >= 0 and check_space(game["grid"], row, column):
            game["active_column"] = column
            refresh_board(self)

    def action_move_right(self) -> None:
        """move the falling block one column to the right"""
        if (not game.get("started") or game.get("paused") or game.get("active_row") is None):
            return

        row = game["active_row"]
        column = game["active_column"] + 1

        if (column < game["columns"] and check_space(game["grid"], row, column)):
            game["active_column"] = column
            refresh_board(self)

    def action_quit_game(self) -> None:
        if game.get("started"):
            finish_game(self)
        self.exit()

if __name__ == "__main__":
    TetrisApp().run()
