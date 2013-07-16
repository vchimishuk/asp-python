import sys
import curses
import libchub
import time

from gui.controller import Controller
from gui import command


client = libchub.Client()

try:
    client.connect("localhost", 1488)
except libchub.ConnectionError as e:
    print('Connection failed. ' + str(e))
    sys.exit(1)


def main(stdscr):
    #stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    #stdscr.keypad(True)
    stdscr.refresh()


    controller = Controller(client)

    while True:
        key = stdscr.getch()
        cmd = command.translate_curses_key(key)

        if cmd == command.CMD_QUIT:
            break
        elif cmd is not None:
            controller.on_command(cmd)
        else:
            raise Exception('key: ' + str(key))


curses.wrapper(main)
