# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jeffrey"
__date__ ="$Nov 20, 2009 8:39:22 PM$"

import threading

if __name__ == "__main__":
    import curses
    stdscr = curses.initscr()
    curses.echo()
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    
    for i in range(80):
        stdscr.addstr(0, i, '=')
        

    while 1:
        c = stdscr.getch()
        if c == ord('p'): PrintDocument()
        elif c == ord('q'): break  # Exit the while()
        elif c == curses.KEY_HOME: x = y = 0

    curses.endwin()