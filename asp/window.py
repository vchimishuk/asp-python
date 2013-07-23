#from acurses import Panel
import acurses


class Window:
    """
    UI windows base class implementation.
    """
    def __init__(self, x, y, width, height):
        self.win = acurses.Panel(x, y, width, height)

    def top(self):
        self.win.top()

    def refresh(self):
        self.win.refresh()

    def subwin(self, x, y, width, height):
        return self.win.subwin(x, y, width, height)

    def write(self, x, y, text, maxlen=None):
        self.win.write(x, y, text, maxlen)

    @property
    def x(self):
        return self.win.x

    @property
    def y(self):
        return self.win.y

    @property
    def width(self):
        return self.win.width

    @property
    def height(self):
        return self.win.height
