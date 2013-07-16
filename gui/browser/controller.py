import os
from gui import command
from gui.basecontroller import BaseController
from libchub.entry import Directory


class Controller(BaseController):
    """
    Browser controller handles commands addressed to the browser window.
    """
    def __init__(self, window, client):
        super().__init__(window)

        self.client = client

        self.register_command(command.CMD_BACK, self.cmd_back)
        self.register_command(command.CMD_DOWN, self.cmd_down)
        self.register_command(command.CMD_ENTER, self.cmd_enter)
        self.register_command(command.CMD_UP, self.cmd_up)

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
