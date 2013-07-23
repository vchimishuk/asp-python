import curses


BLACK = curses.COLOR_BLACK
BLUE = curses.COLOR_BLUE
CYAN = curses.COLOR_CYAN
GREEN = curses.COLOR_GREEN
MAGENTA = curses.COLOR_MAGENTA
RED = curses.COLOR_RED
WHITE = curses.COLOR_WHITE
YELLOW = curses.COLOR_YELLOW


def init_pair(n, fg, bg):
    curses.init_pair(n, fg, bg)


def color_pair(n):
    return curses.color_pair(n)
