#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

"""
based on https://stackoverflow.com/a/26176680/1164295
"""

import curses, curses.panel # https://docs.python.org/3/howto/curses.html
import datetime
import random
import time
import sys
import select # https://docs.python.org/3/library/select.html
import json

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
        # name=None
        # get_name=False
        while self.running :
            this_time = datetime.datetime.today()+datetime.timedelta(minutes=self.count)
            time_str = datetime.datetime.strftime(this_time, "%Y-%m-%d %H:%M") # https://strftime.org/

            # initial read
            with open("state.json",'r') as file_handle:
                state_data = json.load(file_handle)

            # make modifications based on config
            if 'app' in state_data.keys():
                if 'dur' in state_data.keys():
                    state_data['dur'] += 1
                    if state_data['dur']>10:
                        state_data = {'state':'on'}
                    with open("state.json",'w') as file_handle:
                        json.dump(state_data,file_handle)
            if 'd' in state_data.keys():
                if 'dur' in state_data.keys():
                    state_data['dur'] += 1
                    if state_data['dur']>10:
                        state_data = {'state':'on'}
                    with open("state.json",'w') as file_handle:
                        json.dump(state_data,file_handle)


            # # reload state
            # with open("state.json",'r') as file_handle:
            #     state_data = json.load(file_handle)

            if state_data['state']=='on':
                p = int(round(random.random()*9))+3
                if 'app' in state_data.keys():
                    if state_data['app']=='running':
                        p = p + int(round(random.random()*100))+20
            else:
                p = 0

            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                # get_name=False
                line = sys.stdin.read(1)
                if line.strip() == "q": # quit
                    self.stop()
                    self.ui.quit_ui()
                    break
                elif line.strip() == "s": # switch
                    self.ui.switch_pan()
                elif line.strip() == "p": # cycle
                    if state_data['state']=='on':
                        with open("state.json",'w') as file_handle:
                            json.dump({'state':'off'},file_handle)
                    elif state_data['state']=='off':
                        with open("state.json",'w') as file_handle:
                            json.dump({'state':'on'},file_handle)
                    else:
                        raise Exception("Invalid state in state.json; should be 'on' or 'off'")
                elif line.strip() == "r": # run
                    with open("state.json",'w') as file_handle:
                        json.dump({'state':'on','app':'running','dur': 0},file_handle)
                elif line.strip() == "t": # terminate
                    with open("state.json",'w') as file_handle:
                        json.dump({'state':'on','app':'inactive'},file_handle)
                elif line.strip() == "d": #
                    with open("state.json",'w') as file_handle:
                        json.dump({'state':'on','d':'running','dur': 0},file_handle)



            # populate the window with random content that is dynamically changing
            if self.ui.pan2.hidden() and self.ui.pan3.hidden(): # 1 is shown
                self.ui.win1.erase() # https://stackoverflow.com/a/43486979/1164295
                self.ui.win1.border(0)
                self.ui.win1.addstr(1, 1, "Window 1")
                self.ui.win1.addstr(3, 1, str(time_str)+" | p: "+str(p))
                #self.ui.win1.addstr(4, 1, str(self.running))
                self.ui.win1.addstr(4, 1, str(state_data))

                self.ui.win_ctrl.erase()
                self.ui.win_ctrl.border(0)
                self.ui.win_ctrl.addstr(1, 1, "Control panel")
                self.ui.win_ctrl.addstr(3, 1, "Press 's' to switch windows; 'q' to quit;")
                if state_data['state']=='on':
                    self.ui.win_ctrl.addstr(4, 1, "'p' to turn off")
                    self.ui.win_ctrl.addstr(5, 1, "'d' to d")
                elif state_data['state']=='off':
                    self.ui.win_ctrl.addstr(4, 1, "'p' to turn on")
                else:
                    raise Exception("Invalid state in state.json; should be 'on' or 'off'")

                self.ui.win_ctrl.addstr(8, 1, "Don't kill this using ctrl+c or ctrl-z")


            if self.ui.pan1.hidden() and self.ui.pan3.hidden(): # 2 is shown
                self.ui.win2.erase() # https://stackoverflow.com/a/43486979/1164295
                self.ui.win2.border(0)
                self.ui.win2.addstr(1, 1, "Window 2")
                self.ui.win2.addstr(3, 1, str(time_str))#+": "+str(p)) # don't show `p` in win2
                #self.ui.win2.addstr(4, 1, str(self.running))
                self.ui.win2.addstr(4, 1, str(state_data))

                self.ui.win_ctrl.erase()
                self.ui.win_ctrl.border(0)
                self.ui.win_ctrl.addstr(1, 1, "Control panel")
                self.ui.win_ctrl.addstr(3, 1, "Press 's' to switch windows; 'q' to quit;")
                if state_data['state']=='on':
                    if 'app' in state_data.keys():
                        if state_data['app']=='running':
                            self.ui.win_ctrl.addstr(4, 1, "'t' to terminate")
                        else: # not running
                            self.ui.win_ctrl.addstr(4, 1, "'r' to run")
                    else: # on but no app
                        self.ui.win_ctrl.addstr(4, 1, "'r' to run")

                elif state_data['state']=='off':
                    pass
                else:
                    raise Exception("Invalid state in state.json; should be 'on' or 'off'")

                # self.ui.win_ctrl.addstr(5, 1, "'n' to name")
                # https://stackoverflow.com/a/21785167/1164295
                # if get_name:
                #     self.ui.win_ctrl.addstr(7,0,"name:")
                #     name = str(self.ui.win_ctrl.getstr(7,6, 25))
                # if name:
                #     self.ui.win_ctrl.addstr(7,0,"name:"+name)

                self.ui.win_ctrl.addstr(8, 1, "Don't kill this using ctrl+c or ctrl-z")


            if self.ui.pan1.hidden() and self.ui.pan2.hidden(): # 3 is shown
                self.ui.win3.erase() # https://stackoverflow.com/a/43486979/1164295
                self.ui.win3.border(0)
                self.ui.win3.addstr(1, 1, "Window 3")
                self.ui.win3.addstr(3, 1, time_str+\
                                    ": "+str(int(round(random.random()*99999999))))
                #self.ui.win3.addstr(4, 1, str(self.running))
                self.ui.win3.addstr(4, 1, str(state_data))

                self.ui.win_ctrl.erase()
                self.ui.win_ctrl.border(0)
                self.ui.win_ctrl.addstr(1, 1, "Control panel")
                self.ui.win_ctrl.addstr(3, 1, "Press 's' to switch windows; 'q' to quit;")
                self.ui.win_ctrl.addstr(8, 1, "Don't kill this using ctrl+c or ctrl-z")


            self.ui.refresh()
            time.sleep(0.5)
            self.count += 1

if __name__ == "__main__":
    with open("state.json",'w') as file_handle:
        json.dump({'state':'off'},file_handle)

    f = feeder()
    f.run()

    # possible TODO: use curses.wrapper() to handle exceptions. 
    # See <https://www.devdungeon.com/content/curses-programming-python>

# EOF
