#!/usr/bin/env python3

"""
https://docs.python.org/3/howto/curses.html
"""

import curses
import time

##### Begin boilerplate for curses configuration #####

# Before doing anything, curses must be initialized. This is done by calling the initscr() function, which will determine the terminal type, send any required setup codes to the terminal, and create various internal data structures. If successful, initscr() returns a window object representing the entire screen; this is usually called stdscr after the name of the corresponding C variable.
stdscr = curses.initscr()

# Usually curses applications turn off automatic echoing of keys to the screen, in order to be able to read keys and only display them under certain circumstances. This requires calling the noecho() function.
curses.noecho()

# Applications will also commonly need to react to keys instantly, without requiring the Enter key to be pressed; this is called cbreak mode, as opposed to the usual buffered input mode.
curses.cbreak()

# Terminals usually return special keys, such as the cursor keys or navigation keys such as Page Up and Home, as a multibyte escape sequence. While you could write your application to expect such sequences and process them accordingly, curses can do it for you, returning a special value such as curses.KEY_LEFT. To get curses to do the job, you’ll have to enable keypad mode.
stdscr.keypad(True)

##### End boilerplate for curses configuration #####

def watch_me():
    val = 4
    return val

def main(stdscr):
    # Clear screen
#    stdscr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)


    # Coordinates are always passed in the order y,x, and the top-left corner of a window is coordinate (0,0).
    win_begin_x = 20; win_begin_y = 7
    win_height = 5; win_width = 40
    # valid coordinates extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).
    win = curses.newwin(win_height, win_width, win_begin_y, win_begin_x)

    win.addstr(0,0, "RED ALERT!", curses.color_pair(1))

    while True:
        stdscr.addstr(0,0, str(watch_me()))
        win.refresh()

        stdscr.refresh()
        stdscr.getkey()
        time.sleep(1)

# call main
curses.wrapper(main)



# Terminating a curses application is much easier than starting one. 
# to reverse the curses-friendly terminal settings, 
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
# call the endwin() function to restore the terminal to its original operating mode.

curses.endwin()

