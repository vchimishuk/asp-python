import curses
from curses import panel
from gui.basewindow import BaseWindow


class Window(BaseWindow):
    """
    Playlists screen window.
    """
    def __init__(self, height, width, y, x):
        super().__init__(height, width, y, x)

        max_y, max_x = self.window.getmaxyx()

        self.tabs_win = self.window.subwin(1, max_x, 0, 0)
        self.list_win = self.window.subwin(max_y - 1, max_x, 1, 0)

        # XXX:
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLUE)
        BG1 = curses.color_pair(10)
        self.tabs_win.bkgd(' ', BG1)
        curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.BG2 = curses.color_pair(11)
        #self.entries_win.bkgd(' ', BG2)

    def refresh(self):
        """
        Redraw window.
        """
        super().refresh()

        self.tabs_win.refresh()
        self.list_win.refresh()

    def set_playlists(self, plists):
        """
        Set available playlists list.
        """
        self.tabs_win.erase()
        self.tabs_win.addstr(0, 1, str(plists))
