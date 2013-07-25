import acurses


class Window:
    """
    UI windows base class implementation.
    """
    def __init__(self, x, y, width, height, parent=None):
        if parent:
            self.win = parent.subwin(x, y, width, height)
        else:
            self.win = acurses.Panel(x, y, width, height)

    def top(self):
        self.win.top()

    def erase(self):
        self.win.erase()

    def refresh(self):
        self.win.refresh()

    def subwin(self, x, y, width, height):
        return Window(x, y, width, height, self.win)

    def textbox(self):
        return acurses.Textbox(self.win)

    def write(self, x, y, text, color=None, maxlen=None):
        self.win.write(x, y, text, color, maxlen)

    def set_background(self, c):
        self.win.bkgd(c)

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
