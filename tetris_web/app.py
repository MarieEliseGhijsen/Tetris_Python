
import random
from time import monotonic

from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "fhdsjhgkjsadghhgdshdgdsngjdsfnvjdf njdfnvngdfkgjndfgj" #Flask uses this do session

DEFAULT_COLUMNS = 5
DEFAULT_ROWS = 10

MIN_SIZE = 3
MAX_SIZE = 10

COLOURS = [ "red", "blue", "yellow", "green", "black", "orange", ]

#GAME GRID FUNCTIONS
def build_clean_grid(rows, columns):
    return [[None for column in range(columns)] for row in range(rows)]

def check_space(grid, row, column):
    return grid[row][column] is None

def drop_block(grid, row, column, colour):
    grid[row][column] = colour

def clear_full_rows(grid):
    columns = len(grid[0])
    rows = len(grid)

    remaining_rows = [row for row in grid if not all(cell is not None for cell in row)]
    cleared = rows - len(remaining_rows)
    
    empty_rows = [ [None for column in range(columns)] for row in range(cleared) ]
    grid[:] = empty_rows + remaining_rows

    return cleared

#GAME FUNCTIONS
def spawn_block(game):
    grid = game["grid"]
    columns = game["columns"]

    available_columns = [ column for column in range(columns) if check_space(grid, 0, column) ]

    if not available_columns:
        finish_game(game)
        return

    game["active_row"] = 0
    game["active_column"] = random.choice(available_columns)
    game["active_colour"] = random.choice(COLOURS)

def calculate_score(blocks, elapsed, rows, columns):
    return ( blocks * 100 + int(elapsed) * 2 + rows * columns * 5 )

def update_clock(game):
    if not game["started"] or game["paused"]:
        return

    game["elapsed"] = monotonic() - game["start_time"]

def start_game(name, rows, columns):
    game = {
        "name": name,
        "rows": rows,
        "columns": columns,
        "grid": build_clean_grid(rows, columns),

        "blocks": 0,
        "elapsed": 0.0,
        "start_time": monotonic(),

        "started": True,
        "paused": False,
        "over": False,

        "active_row": None,
        "active_column": None,
        "active_colour": None,
    }

    spawn_block(game)

    return game

def game_tick(game):
    if not game["started"] or game["paused"]:
        return

    if game["active_row"] is None:
        spawn_block(game)

    if not game["started"]:
        return

    grid = game["grid"]
    row = game["active_row"]
    column = game["active_column"]

    next_row = row + 1

    if (next_row >= game["rows"] or not check_space(grid, next_row, column)):
        drop_block( grid, row, column, game["active_colour"])
        game["blocks"] += 1
        clear_full_rows(grid)

        game["active_row"] = None
        game["active_column"] = None
        game["active_colour"] = None

        spawn_block(game)

    else:
        game["active_row"] = next_row

    update_clock(game)

def move_block(game, direction):
    if ( not game["started"] or game["paused"] or game["active_row"] is None ):
        return

    row = game["active_row"]
    column = game["active_column"]

    if direction == "left":
        column -= 1
    elif direction == "right":
        column += 1
    else:
        return

    if (0 <= column < game["columns"] and check_space(game["grid"], row, column)):
        game["active_column"] = column

def pause_game(game):
    if game["started"] and not game["paused"]:
        update_clock(game)
        game["paused"] = True

def resume_game(game):
    if game["started"] and game["paused"]:
        game["start_time"] = monotonic() - game["elapsed"]
        game["paused"] = False

def finish_game(game):
    if not game["started"] or game["over"]:
        return

    update_clock(game)

    game["started"] = False
    game["paused"] = False
    game["over"] = True

    game["score"] = calculate_score(
        game["blocks"],
        game["elapsed"],
        game["rows"],
        game["columns"]
    )

#HELPER FUNCTION
def save_game():
    session.modified = True

#FLASK STUFF
@app.get("/")
@app.get("/join")
def show_the_form():
    return render_template(
        "form.html",
        the_title="Tetris - Game Setup",
        default_rows=DEFAULT_ROWS,
        default_columns=DEFAULT_COLUMNS
    )

@app.post("/start")
def start():
    name = request.form.get("the_name", "").strip() #gets values submitted by HTML form
    #strip() removes spaces from start and end

    try: #convert row and column values to int
        rows = int(request.form.get("the_rows", ""))
        columns = int(request.form.get("the_columns", ""))
    except ValueError: #re-run form
        return render_template(
            "form.html",
            the_title="Tetris - Game Setup",
            default_rows=DEFAULT_ROWS,
            default_columns=DEFAULT_COLUMNS,
            message="Rows and columns must be whole numbers.",
            name=name
        )

    if not name:
        return render_template(
            "form.html",
            the_title="Tetris - Game Setup",
            default_rows=DEFAULT_ROWS,
            default_columns=DEFAULT_COLUMNS,
            message="Please enter your name."
        )

    if not MIN_SIZE <= rows <= MAX_SIZE:
        return render_template(
            "form.html",
            the_title="Tetris - Game Setup",
            default_rows=DEFAULT_ROWS,
            default_columns=DEFAULT_COLUMNS,
            message="Rows must be between 3 and 10.",
            name=name
        )

    if not MIN_SIZE <= columns <= MAX_SIZE:
        return render_template(
            "form.html",
            the_title="Tetris - Game Setup",
            default_rows=DEFAULT_ROWS,
            default_columns=DEFAULT_COLUMNS,
            message="Columns must be between 3 and 10.",
            name=name
        )

    session["game"] = start_game(name, rows, columns)

    return redirect(url_for("show_game")) #url_for() find URL using function name

@app.get("/game")
def show_game():
    game = session.get("game")

    if not game: #if no game - ste up
        return redirect(url_for("show_the_form"))

    return render_template(
        "game.html",
        the_title="Tetris",
        game=game
    )

@app.get("/tick")
def tick(): #HTMX requests this continuously while game running
    game = session.get("game")

    if not game:
        return redirect(url_for("show_the_form"))

    game_tick(game)
    save_game()

    return render_template(
        "snippet.html",
        game=game
    )

@app.post("/move/<direction>")
def move(direction):
    game = session.get("game")

    if not game:
        return redirect(url_for("show_the_form"))

    move_block(game, direction)
    save_game()

    return render_template(
        "snippet.html",
        game=game
    )

@app.post("/pause")
def pause():
    game = session.get("game")

    if game:
        pause_game(game)
        save_game()

    return render_template(
        "snippet.html",
        game=game
    )

@app.post("/resume")
def resume():
    game = session.get("game")

    if game:
        resume_game(game)
        save_game()

    return render_template(
        "snippet.html",
        game=game
    )

@app.post("/end")
def end():
    game = session.get("game")

    if not game:
        return redirect(url_for("show_the_form"))

    finish_game(game)
    save_game()

    return render_template(
        "snippet.html",
        game=game
    )

if __name__ == "__main__":
    app.run(debug=True)