import curses
from curses import panel
from curses import textpad


class Window:
    """
    Curses window class wrapper.
    """
    def __init__(self, x, y, width, height, parent=None):
        if parent:
            self.win = parent.win.subwin(height, width, parent.y + y, parent.x + x)
        else:
            self.win = curses.newwin(height, width, y, x)

    def subwin(self, x, y, width, height):
        return Window(x, y, width, height, self)

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

    def bkgd(self, color):
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
        y, x = self.win.getbegyx()

        return y

    @property
    def x(self):
        y, x = self.win.getbegyx()

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


class CursesTextbox(textpad.Textbox):
    """
    Curses Textbox improvement wrapper class.
    """
    def do_command(self, ch):
        if ch == curses.ascii.BEL or ch == curses.ascii.ESC: # ^G or Escape
            # Clear input.
            super().do_command(curses.ascii.SOH)
            super().do_command(curses.ascii.VT)

            return False
        elif ch == curses.ascii.NL: # ^J
            return False
        else:
            return super().do_command(ch)


class Textbox:
    """
    Curses Textbox object wrapper.
    """
    def __init__(self, win):
        self.win = win
        self.textbox = CursesTextbox(win.win)

    def edit(self):
        s = self.textbox.edit()
        self.win.erase()
        self.win.refresh()

        return s
