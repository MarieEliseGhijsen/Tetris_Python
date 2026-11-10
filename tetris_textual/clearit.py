
import sys
import time

def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")    # ANSI escape which clears the current terminal screen.
    sys.stdout.flush()

print("Some text which appears on the screen...")

time.sleep(0.5)
clear_the_terminal()

print("Ta da!!!")