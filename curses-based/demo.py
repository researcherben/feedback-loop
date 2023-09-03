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

        # Panel functions allow the use of stacked windows and ensure the proper
        # portions of each window and the curses stdscr window are hidden or
        # displayed when panels are added, moved, modified or removed.

        # Coordinates are always passed in the order y,x
        # The top-left corner of a window is coordinate (0,0).
        # Valid coordinates extend from (0,0) to (curses.LINES - 1, curses.COLS - 1).
        active_data_window_height = 14
        active_data_window_length = 100
        self.win1 = curses.newwin(active_data_window_height, active_data_window_length, 0, 0)
        self.win1.border(0)
        # self.win1.addstr(1, 1, "Win 1")
        self.pan1 = curses.panel.new_panel(self.win1)

        self.win2 = curses.newwin(active_data_window_height, active_data_window_length, 0, 0)
        self.win2.border(0)
        #self.win2.addstr(1, 1, "           A Window 2")
        self.pan2 = curses.panel.new_panel(self.win2)
        self.pan2.hide() # https://docs.python.org/3/library/curses.panel.html

        self.win3 = curses.newwin(active_data_window_height, active_data_window_length, 0, 0)
        self.win3.border(0)
        #self.win3.addstr(1, 1, "And now Window 3")
        self.pan3 = curses.panel.new_panel(self.win3)
        self.pan3.hide() # https://docs.python.org/3/library/curses.panel.html

        self.win_ctrl = curses.newwin(10, 50, active_data_window_height+1, 0)
        self.win_ctrl.border(0)
        self.win_ctrl.addstr(1, 1, "Control panel")
        self.win_ctrl.addstr(3, 1, "Press 's' to switch windows or 'q' to quit.")
        self.win_ctrl.addstr(8, 1, "Don't kill this using ctrl+c or ctrl-z")
        self.pan_ctrl = curses.panel.new_panel(self.win_ctrl)


    def refresh(self):
        """
        `erase` vs `clear`: https://stackoverflow.com/a/43486979/1164295
        """
        # self.win1.erase()
        # self.win1.clear()
        # curses.panel.update_panels() # https://docs.python.org/3/library/curses.panel.html
        # most recent (bottom of this list) is displayed
        self.win1.refresh()
        self.win2.refresh()
        self.win3.refresh()
        self.win_ctrl.refresh()
        #curses.doupdate()

    def switch_pan(self):
        # self.win1.addstr(5, 1, "top_panel: "+str(curses.panel.top_panel()))
        # self.win2.addstr(5, 1, "top_panel: "+str(curses.panel.top_panel()))
        # self.win3.addstr(5, 1, "top_panel: "+str(curses.panel.top_panel()))
        # self.win1.addstr(6, 1, "switchin (win1)")
        # self.win2.addstr(7, 1, "   switchin (win2)")
        # self.win3.addstr(8, 1, "      switchin  (win3)")

        # self.win1.addstr(10, 1, "pan1:"+str(self.pan1.hidden())+", pan2:"+str(self.pan2.hidden())+", pan3:"+str(self.pan3.hidden()))
        # self.win2.addstr(11, 1, "pan1:"+str(self.pan1.hidden())+", pan2:"+str(self.pan2.hidden())+", pan3:"+str(self.pan3.hidden()))
        # self.win3.addstr(12, 1, "pan1:"+str(self.pan1.hidden())+", pan2:"+str(self.pan2.hidden())+", pan3:"+str(self.pan3.hidden()))

         # https://docs.python.org/3/library/curses.panel.html
        if self.pan2.hidden() and self.pan3.hidden(): # 1 is shown, switch to 2
            self.pan2.top()
            self.pan2.show()
            self.pan1.bottom()
            self.pan1.hide()
            self.pan3.bottom()
            self.pan3.hide()
        elif self.pan1.hidden() and self.pan3.hidden(): # 2 is shown, switch to 3
            self.pan3.top()
            self.pan3.show()
            self.pan1.bottom()
            self.pan1.hide()
            self.pan2.bottom()
            self.pan2.hide()
        elif self.pan1.hidden() and self.pan2.hidden(): # 3 is shown, switch to 1
            self.pan1.top()
            self.pan1.show()
            self.pan2.bottom()
            self.pan2.hide()
            self.pan3.bottom()
            self.pan3.hide()
        # else:
        #     print("error")
        #     pass

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
        print("UI terminated\n")
        exit(0)


class feeder:
    # Fake UI feeder
    def __init__(self):
        self.running = False
        self.ui = ui()
        self.count = 0 # tick

    def stop(self):
        """
        stop the update loop
        """
        self.running = False

    def run(self):
        """
        run the update loop
        """
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

            # populate the window with random content that is dynamically changing
            if self.ui.pan2.hidden() and self.ui.pan3.hidden(): # 1 is shown
                self.ui.win1.erase()
                self.ui.win1.border(0)
                self.ui.win1.addstr(1, 1, "Window 1")
                self.ui.win1.addstr(3, 1, str(self.count)+\
                                 ": "+str(int(round(random.random()*99))))
                self.ui.win1.addstr(4, 1, str(self.running))

            if self.ui.pan1.hidden() and self.ui.pan3.hidden(): # 2 is shown
                self.ui.win2.erase()
                self.ui.win2.border(0)
                self.ui.win2.addstr(1, 1, "Window 2")
                self.ui.win2.addstr(3, 1, str(self.count)+\
                                    ": "+str(int(round(random.random()*9999))))
                self.ui.win2.addstr(4, 1, str(self.running))

            if self.ui.pan1.hidden() and self.ui.pan2.hidden(): # 3 is shown
                self.ui.win3.erase()
                self.ui.win3.border(0)
                self.ui.win3.addstr(1, 1, "Window 3")
                self.ui.win3.addstr(3, 1, str(self.count)+\
                                    ": "+str(int(round(random.random()*99999999))))
                self.ui.win3.addstr(4, 1, str(self.running))

            self.ui.refresh()
            time.sleep(0.5)
            self.count += 1

if __name__ == "__main__":
    f = feeder()
    f.run()
