import curses
from acurses import color
from acurses import key
from acurses.window import Window, Panel


__all__ = ['Window', 'Panel',
           'wrapper', 'echo', 'cbreak', 'cursor',
           'color', 'key']


def wrapper(fn):
    curses.wrapper(fn)


def echo(e):
    if e:
        curses.echo()
    else:
        curses.noecho()


def cbreak():
    curses.cbreak()


def cursor(show):
    curses.curs_set(int(show))
