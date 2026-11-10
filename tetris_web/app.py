
import random

from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = "fhdsjhgkjsadghhgdshdgdsngjdsfnvjdf njdfnvngdfkgjndfgj"

COLOURS = [ "red", "blue", "yellow", "green", "black", "orange", ]

#######################################################################
#user chooses row, columns and name
@app.get("/")
@app.get("/data")
def show_the_form():
    return render_template(
        "process.html",
        the_title="Player Join",
        name=session.get("remembered_name", ""),
    )

@app.post("/process")
def process_the_form():
    session["remembered_name"] = request.form["the_name"]
    with open("secrets.txt", "a") as fh:
        print(
            f'{request.form["the_name"]},{request.form["the_age"]},{request.form["the_password"]}',
            file=fh
        )
    return render_template(
        "data.html",
        the_title="Ah ha!",
        name=request.form["the_name"],
        age=request.form["the_age"],
        password=request.form["the_password"],
    )
#######################################################################

@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    return render_template( "grid.html", rowcount=8, colcount=4, colour="white", )

@app.post("/location/<row>/<col>/<colour>")
def process_the_click(row, col, colour):
    set_colour = "white" if colour != "white" else random.choice(COLOURS)
    return render_template( "snippet.html", row=row, col=col, colour=set_colour, )

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
#when game over record name, time played and score (calculate)