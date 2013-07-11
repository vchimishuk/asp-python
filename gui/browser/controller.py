import os
from gui import command
from gui.basecontroller import BaseController
from libchub.entry import Directory


class Controller(BaseController):
    """
    Browser controller handles commands addressed to the browser window.
    """
    def __init__(self, window, client):
        super().__init__()

        self.window = window
        self.client = client

        self.register_command(command.CMD_BACK, self.back)
        self.register_command(command.CMD_DOWN, self.down)
        self.register_command(command.CMD_ENTER, self.enter)
        self.register_command(command.CMD_UP, self.up)

    # TODO: Save stack of the last selected path history.
    def set_path(self, path):
        up_path = os.path.normpath(os.path.join(path, '..'))
        up = Directory('..', up_path)
        self.entries = [up] + self.client.ls(path)
        self.selected = 0

        self.window.set_path(path)
        self.window.set_selected(self.selected)
        self.window.set_entries(self.entries)
        self.window.refresh()

    def down(self):
        if self.selected + 1 < len(self.entries):
            self.selected += 1
            self.window.set_selected(self.selected)
            self.window.refresh()

    def up(self):
        if self.selected > 0:
            self.selected -= 1
            self.window.set_selected(self.selected)
            self.window.refresh()

    def enter(self):
        if len(self.entries):
            e = self.entries[self.selected]
            if isinstance(e, Directory):
                self.set_path(e.path)
            else:
                # TODO: Play track.
                pass

    def back(self):
        updir = self.entries[0]
        self.set_path(updir.path)
