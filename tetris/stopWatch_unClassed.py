from time import monotonic #helps measure time

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header

timers = {} #stores data for stopwatches using ids
next_id = 0 #assign own id to each stopwatch

def format_time(elapsed):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"

def update_time(app, timer_id):
    if timer_id not in timers:
        return

    timer = timers[timer_id]

    if timer["running"]:
        elapsed = timer["total"] + monotonic() - timer["start_time"]
        app.query_one(f"#display-{timer_id}", Digits).update(format_time(elapsed) # display formatted time

def add_stopwatch(app):
    global next_id

    timer_id = next_id
    next_id += 1 #give new own id

    timers[timer_id] = { "start_time": 0.0, "total": 0.0, "running": False, } #set new id

    #create stopwatch elements
    app.query_one("#timers").mount(HorizontalGroup(Button("Start", id=f"start-{timer_id}"), Button("Stop", id=f"stop-{timer_id}"), Button("Reset", id=f"reset-{timer_id}"), Digits("00:00:00.00", id=f"display-{timer_id}"), id=f"timer-{timer_id}", classes="stopwatch",))
    app.query_one(f"#stop-{timer_id}").display = False

    app.set_interval(1 / 60,lambda tid=timer_id: update_time(app, tid),)

def remove_stopwatch(app):
    stopwatch_widgets = app.query("#timers > HorizontalGroup")

    if stopwatch_widgets:
        widget = stopwatch_widgets.last()
        timer_id = int(widget.id.split("-")[1])
        widget.remove()
        timers.pop(timer_id, None)

def remove_stopwatch(app):
    stopwatch_widgets = app.query("#timers > HorizontalGroup")

    if stopwatch_widgets: #remove stopWatch if exists
        widget = stopwatch_widgets.last()
        timer_id = int(widget.id.split("-")[1])
        widget.remove()
        timers.pop(timer_id, None)


def on_button_pressed(app, event):
    button_id = event.button.id #get id of button pressed
    if not button_id:
        return

    action, timer_id = button_id.split("-", 1)
    timer_id = int(timer_id)
    if timer_id not in timers:
        return

    timer = timers[timer_id]
    widget = app.query_one(f"#timer-{timer_id}")

    #update stopwatch
    if action == "start" and not timer["running"]:
        timer["start_time"] = monotonic()
        timer["running"] = True
        widget.add_class("started")

    elif action == "stop" and timer["running"]:
        timer["total"] += monotonic() - timer["start_time"]
        timer["running"] = False
        widget.remove_class("started")
        update_time(app, timer_id)

    elif action == "reset":
        timer["total"] = 0.0

        if timer["running"]:
            timer["start_time"] = monotonic()

        app.query_one(f"#display-{timer_id}", Digits).update("00:00:00.00")

def toggle_dark(app):
    app.theme = ("textual-dark" if app.theme == "textual-light" else "textual-light")

def toggle_dark(app):
    app.theme = ("textual-dark"if app.theme == "textual-light"else "textual-light")

def compose():
    yield Header()
    yield Footer()
    yield VerticalScroll(id="timers")

def toggle_dark(app):
    app.theme = (
        "textual-dark"
        if app.theme == "textual-light"
        else "textual-light"
    )

def compose():
    yield Header()
    yield Footer()
    yield VerticalScroll(id="timers")

app = App() #make a textual app

app.compose = compose

app.on_button_pressed = lambda event: on_button_pressed(app, event)

app.action_add_stopwatch = lambda: add_stopwatch(app)
app.action_remove_stopwatch = lambda: remove_stopwatch(app)
app.action_toggle_dark = lambda: toggle_dark(app)

#set keyboard shortcuts
app.BINDINGS = [ ("d", "toggle_dark", "Toggle dark mode"), ("a", "add_stopwatch", "Add"), ("r", "remove_stopwatch", "Remove"), ]
app.CSS_PATH = "stopWatchCSS.tcss"

def on_mount():
    add_stopwatch(app)
    add_stopwatch(app)
    add_stopwatch(app)

app.on_mount = on_mount

app.run()
