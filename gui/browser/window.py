import curses


class Window:
    """
    Filesystem browser window.
    """
    def __init__(self, height, width, y, x):
        self.win = curses.newwin(height, width, y, x)
        max_y, max_x = self.win.getmaxyx()

        self.path_win = self.win.subwin(1, max_x, 0, 0)
        self.entries_win = self.win.subwin(max_y - 1, max_x, 1, 0)

        self.selected = 0
        self.entries = []

        # XXX:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
        BG1 = curses.color_pair(1)
        self.path_win.bkgd(' ', BG1)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        self.BG2 = curses.color_pair(2)
        #self.entries_win.bkgd(' ', BG2)
        
    def refresh(self):
        """
        Redraw window.
        """
        self.win.refresh()
        self.path_win.refresh()
        self.entries_win.refresh()

    def set_path(self, path):
        """
        Set path string in the window title.
        """
        # TODO: Truncate long title from the beginning.
        self.path_win.erase()
        self.path_win.addstr(0, 1, path)

    def set_entries(self, entries):
        """
        Set displaying folder content.
        """
        self.entries_win.erase()

        self.entries = entries

        # TODO: Set entry formatter via setter.
        for y in range(len(entries)):
            s = str(entries[y])

            if self.selected == y:
                self.entries_win.addstr(y, 1, s, self.BG2)
            else:
                self.entries_win.addstr(y, 1, s)

    def set_selected(self, i):
        """
        Set index of the selected item.
        """
        self.selected = i
        self.set_entries(self.entries)
