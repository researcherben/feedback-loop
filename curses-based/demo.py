#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

"""
from https://stackoverflow.com/a/26176680/1164295
"""

import curses, curses.panel
import random
import time
import sys
import select

# gui = None

class ui:
    def __init__(self):
        ##### Begin boilerplate for curses configuration #####
        # Before doing anything, curses must be initialized. This is done by
        # calling the initscr() function, which will determine the terminal type,
        # send any required setup codes to the terminal, and create various
        # internal data structures. If successful, initscr() returns a window
        # object representing the entire screen; this is usually called stdscr
        # after the name of the corresponding C variable.
        self.stdscr = curses.initscr()
        # Usually curses applications turn off automatic echoing of keys
        # to the screen, in order to be able to read keys and only display
        # them under certain circumstances. This requires calling the noecho() function.
        curses.noecho()
        # Applications will also commonly need to react to keys instantly,
        # without requiring the Enter key to be pressed; this is called cbreak mode,
        # as opposed to the usual buffered input mode.
        curses.cbreak()
        curses.curs_set(0)
        # # Terminals usually return special keys, such as the cursor keys or
        # navigation keys such as Page Up and Home, as a multibyte escape sequence.
        # While you could write your application to expect such sequences and
        # process them accordingly, curses can do it for you, returning a special
        # value such as curses.KEY_LEFT. To get curses to do the job,
        # you’ll have to enable keypad mode.
        self.stdscr.keypad(True)
        ##### End boilerplate for curses configuration #####

        # Coordinates are always passed in the order y,x,
        # and the top-left corner of a window is coordinate (0,0).
        # # valid coordinates extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).
        self.win1 = curses.newwin(10, 50, 0, 0)
        self.win1.border(0)
        self.win1.addstr(1, 1, "Window 1")
        self.pan1 = curses.panel.new_panel(self.win1)
        self.pan1.hide()

        self.win2 = curses.newwin(10, 50, 0, 0)
        self.win2.border(0)
        self.win2.addstr(1, 1, "Window 2")
        self.pan2 = curses.panel.new_panel(self.win2)

        self.win3 = curses.newwin(10, 50, 12, 0)
        self.win3.border(0)
        self.win3.addstr(1, 1, "Control panel")
        self.win3.addstr(3, 1, "Press 's' to switch windows or 'q' to quit.")
        self.pan3 = curses.panel.new_panel(self.win3)


    def refresh(self):
        curses.panel.update_panels()
        self.win2.refresh()
        self.win1.refresh()

    def switch_pan(self):
        if self.pan1.hidden():
            self.pan2.bottom()
            self.pan2.hide()
            self.pan1.top()
            self.pan1.show()
        else:
            self.pan1.bottom()
            self.pan1.hide()
            self.pan2.top()
            self.pan2.show()

        self.refresh()

    def quit_ui(self):
        # Terminating a curses application is much easier than starting one.
        # to reverse the curses-friendly terminal settings,
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.curs_set(1)
        curses.echo()
        # call the endwin() function to restore the terminal to its original operating mode.
        curses.endwin()
        print("UI terminated")
        exit(0)


class feeder:
    # Fake UI feeder
    def __init__(self):
        self.running = False
        self.ui = ui()
        self.count = 0

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.feed()

    def feed(self):
        while self.running :
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.read(1)
                if line.strip() == "q":
                    self.stop()
                    self.ui.quit_ui()
                    break
                elif line.strip() == "s":
                    self.ui.switch_pan()

            self.ui.win1.addstr(3, 1, str(self.count)+\
                                ": "+str(int(round(random.random()*999))))
            self.ui.win1.addstr(4, 1, str(self.running))
            self.ui.win2.addstr(3, 1, str(self.count)+\
                                ": "+str(int(round(random.random()*999))))
            self.ui.win2.addstr(4, 1, str(self.running))
            self.ui.refresh()
            time.sleep(0.5)
            self.count += 1

if __name__ == "__main__":
    f = feeder()
    f.run()
