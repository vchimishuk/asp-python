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


class ListWindow(Window):
    def __init__(self, parent, x, y, width, height):
        super().__init__(x, y, width, height, parent)

        self.items = []
        # Indexes of the selected, first visible,
        # and next after last visible items.
        self.selected = 0
        self.begin = 0
        self.end = 0

    def page_scope(self, n, selected):
        b = max(selected - self.height // 2, 0)
        e = min(b + self.height, n)

        # If last page is smaller than screen take part of the current one.
        if e - b < self.height:
            e = n
            b = max(e - self.height, 0)

        return b, e

    def set_page(self, s, begin):
        l = len(self.items)
        self.selected = min(max(0, s), l - 1)
        self.begin = max(min(begin, l - self.height), 0)
        self.end = min(self.begin + self.height, l)

        self.redraw()

    def redraw(self):
        self.erase()

        for y in range(self.begin, self.end):
            s = str(y) + ' ' + str(self.items[y])
            c = None

            if self.selected == y:
                c = color.LIST_SELECTED

            self.write(1, y - self.begin, s, c)

    def set_items(self, items):
        self.items = items

        self.set_selected(0)
        self.redraw()

    def get_selected(self):
        return self.selected

    def set_selected(self, i, save_page=False):
        l = len(self.items)
        i = min(i, l - 1)
        i = max(i, 0)

        self.selected = i

        if not save_page or (i < self.begin or i >= self.end):
            self.begin, self.end = self.page_scope(l, self.selected)

        self.redraw()

    def select_next(self):
        self.set_selected(self.selected + 1, True)

    def select_prev(self):
        self.set_selected(self.selected - 1, True)

    def select_next_page(self):
        self.set_page(self.selected + self.height, self.begin + self.height)

    def select_prev_page(self):
        self.set_page(self.selected - self.height, self.begin - self.height)

    def select_first(self):
        self.set_selected(0)

    def select_last(self):
        self.set_selected(len(self.items) - 1)
