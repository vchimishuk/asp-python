import curses
from collections import namedtuple


Configs = namedtuple('Configs', ('host', 'port', 'nport'))

def main(stdscr):
    configs = Configs(host='localhost',
                      port=1488,
                      nport=1489)

    # We must delay all our packages initialization to give native
    # curses chance inialize inteslf properly.
    from application import Application

    app = Application(stdscr, configs)
    app.run()


if __name__ == '__main__':
    curses.wrapper(main)
