import curses
from curses import panel


class Window:
    """
    Curses window class wrapper.
    """
    def __init__(self, x, y, width, height, parent=None):
        if parent:
            self.win = parent.subwin(height, width, y, x)
        else:
            self.win = curses.newwin(height, width, y, x)

    def subwin(self, x, y, width, height):
        return Window(x, y, width, height, self.win)

    def write(self, x, y, text, color=None, maxlen=None):
        args = [y, x, text]

        if color is not None:
            args.append(color.pair)
        if maxlen is not None:
            args.append(maxlen)

        if maxlen:
            self.win.addnstr(*args)
        else:
            self.win.addstr(*args)

    def set_background(self, color):
        self.win.bkgd(' ', color.pair)

    def erase(self):
        self.win.erase()

    def refresh(self):
        self.win.refresh()

    @property
    def width(self):
        y, x = self.win.getmaxyx()

        return x

    @property
    def height(self):
        y, x = self.win.getmaxyx()

        return y

    @property
    def y(self):
        y, x = self.win.getyx()

        return y

    @property
    def x(self):
        y, x = self.win.getyx()

        return x


class Panel(Window):
    """
    Curses panel class wrapper.
    """
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)

        self.panel = panel.new_panel(self.win)

    def top(self):
        self.panel.top()
        panel.update_panels()
        self.refresh()
