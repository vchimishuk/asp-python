import curses
from curses import panel


class BaseWindow:
    def __init__(self, height, width, y, x):
        self.window = curses.newwin(height, width, y, x)
        self.panel = panel.new_panel(self.window)

    def activate(self):
        self.panel.top()
        panel.update_panels()
        self.refresh()

    def refresh(self):
        self.window.refresh()
