
import time
from pynput import keyboard
import queue

key_pressed = None    # This is a global variable.

def process_on_press(key):
    global key_pressed
    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = str(key)

print("We're looping... press the 'q' key to quit.")

listener = keyboard.Listener( on_press=process_on_press )

listener.start()

#while True:
#    if key_pressed:
#        print(f"We got this key: {key_pressed}.")
#        if key_pressed == "q":
#            print("we're done.")
#            break
#        key_pressed = None

#    print("Working...")
#    time.sleep(0.5)

#listener.stop()

