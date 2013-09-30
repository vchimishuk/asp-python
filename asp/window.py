import acurses
import color


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


class ListWindow:
    def __init__(self, parent, x, y, width, height):
        self.win = parent.subwin(x, y, width, height)

        self.items = []
        self.selected = 0

    def refresh(self):
        self.win.refresh()

    def erase(self):
        self.win.erase()

    def set_items(self, items, selected=None):
        self.items = items
        if selected is not None:
            self.selected = selected

        self.erase()

        # TODO: Set entry formatter via setter.
        for y in range(len(items)):
            s = str(items[y])
            c = None

            if self.selected == y:
                c = color.LIST_SELECTED

            self.win.write(1, y, s, c)

    def get_selected(self):
        return self.selected

    def set_selected(self, i):
        self.set_items(self.items, i)

    def select_next(self):
        if self.selected + 1 < len(self.items):
            self.set_items(self.items, self.selected + 1)

    def select_prev(self):
        if self.selected > 0:
            self.set_items(self.items, self.selected - 1)
