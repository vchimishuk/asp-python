import os
import controller
import window
import command
import color
from libchub.entry import Directory


class Controller(controller.Controller):
    NAME = command.BROWSER

    def __init__(self, win, client):
        super().__init__(win)

        self.client = client

        self.register_command(command.BACK, self.cmd_back)
        self.register_command(command.DOWN, self.cmd_down)
        self.register_command(command.ENTER, self.cmd_enter)
        self.register_command(command.UP, self.cmd_up)

        self.path = '/'
        self.selected = 0

    def set_path(self, path, forward=True):
        up_path = os.path.normpath(os.path.join(path, '..'))
        up = Directory('..', up_path)
        self.entries = [up] + self.client.ls(path)

        # Restore selection on navigation back.
        self.selected = 0
        for i in range(len(self.entries)):
            e = self.entries[i]
            if self.is_directory(e) and e.path == self.path:
                self.selected = i
        self.path = path

        self.window.set_path(path)
        self.window.set_selected(self.selected)
        self.window.set_entries(self.entries)
        self.window.refresh()

    def cmd_down(self):
        if self.selected + 1 < len(self.entries):
            self.selected += 1
            self.window.set_selected(self.selected)
            self.window.refresh()

    def cmd_up(self):
        if self.selected > 0:
            self.selected -= 1
            self.window.set_selected(self.selected)
            self.window.refresh()

    def cmd_enter(self):
        e = self.entries[self.selected]
        if self.is_directory(e):
            self.set_path(e.path, self.selected != 0)
        else:
            # TODO: Play track.
            pass

    def cmd_back(self):
        updir = self.entries[0]
        self.set_path(updir.path, False)

    def is_directory(self, e):
        return isinstance(e, Directory)


class Window(window.Window):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.path_win = self.subwin(0, 0, self.width, 1)
        self.path_win.set_background(color.BROWSER_PATH)
        self.list_win = self.subwin(0, 1, self.width, self.height - 1)

        self.selected = 0
        self.entries = []
        
    def refresh(self):
        super().refresh()

        self.path_win.refresh()
        self.list_win.refresh()

    def set_path(self, path):
        self.path_win.erase()
        self.path_win.write(1, 0, path)

    def set_entries(self, entries):
        self.entries = entries
        
        self.list_win.erase()

        # TODO: Set entry formatter via setter.
        for y in range(len(entries)):
            s = str(entries[y])
            c = None

            if self.selected == y:
                c = color.SELECTED

            self.list_win.write(1, y, s, c)

    def set_selected(self, i):
        self.selected = i
        self.set_entries(self.entries)
