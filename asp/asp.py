import curses


def main(stdscr):
    # We must delay all our packages initialization to give native
    # curses chance inialize inteslf properly.
    from application import Application

    app = Application(stdscr)
    app.run()


if __name__ == '__main__':
    curses.wrapper(main)
