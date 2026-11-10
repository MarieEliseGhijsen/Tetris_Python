
import random

from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = "fhdsjhgkjsadghhgdshdgdsngjdsfnvjdf njdfnvngdfkgjndfgj"

COLOURS = [ "red", "blue", "yellow", "green", "black", "orange", ]

#######################################################################

#user chooses row, columns and name
@app.get("/")
@app.get("/join")
def show_the_form():
    return render_template(
        "form.html",
        the_title="Player Join",
    )
    
#######################################################################

#when game over record name, time played and score (calculate)
@app.get("/gameOver")
def display_game_over():
    session["name"] = request.form["the_name"]
    session["rows"] = request.form["the_rows"]
    session["columns"] = request.form["the_columns"]
    return render_template(
        "gameOver.html",
        the_title="Game Over",
        name=session["name"],
        score=(10*100+10*2+int(session["rows"])*int(session["columns"])*5), #blocks * 100 + time * 2 + rows * columns * 5
    )
    
#######################################################################

@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    session["rows"] = request.form["the_rows"]
    session["columns"] = request.form["the_columns"]
    return render_template( "grid.html", the_title="showgrid", rowcount=session["rows"], colcount=session["columns"], colour="white", )

@app.post("/location/<row>/<col>/<colour>")
def process_the_click(row, col, colour):
    set_colour = "white" if colour != "white" else random.choice(COLOURS)
    return render_template( "snippet.html", the_title="location", row=row, col=col, colour=set_colour, )

@app.post("/counting")
def maintain_count():
    session["count"] = session["count"] + 1
    return "Time is ticking: " + str(session["count"])

@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    return f"You pressed: {key_pressed}."

if __name__ == "__main__":
    app.run(debug=True)

#block drops in random column
#block assigned random colour
#block moves left and right
#block stays on bottom of board once dropped
#when row filled it clears