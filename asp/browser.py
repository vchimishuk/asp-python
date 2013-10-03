import os
import controller
import window
import command
import color
from libchub.entry import Directory


class Controller(controller.Controller):
    NAME = command.BROWSER

    def __init__(self, app, win):
        super().__init__(app, win)

        self.register_command(command.ADD, self.cmd_add)
        self.register_command(command.BACK, self.cmd_back)
        self.register_command(command.END, self.cmd_end)
        self.register_command(command.ENTER, self.cmd_enter)
        self.register_command(command.HOME, self.cmd_home)
        self.register_command(command.NEXT, self.cmd_next)
        self.register_command(command.NEXT_PAGE, self.cmd_next_page)
        self.register_command(command.PREV, self.cmd_prev)
        self.register_command(command.PREV_PAGE, self.cmd_prev_page)

        self.path = '/'

    def set_path(self, path, forward=True):
        up_path = os.path.normpath(os.path.join(path, '..'))
        up = Directory({'name': '..', 'path': up_path})
        self.entries = [up] + self.app.client.ls(path)

        # Restore selection on navigation back.
        selected = 0
        for i in range(len(self.entries)):
            e = self.entries[i]
            if self.is_directory(e) and e.path == self.path:
                selected = i
        self.path = path

        self.window.set_path(path)
        self.window.set_selected(selected)
        self.window.set_items(self.entries)
        self.window_refresh()

    def cmd_next(self):
        self.window.select_next()
        self.window_refresh()

    def cmd_prev(self):
        self.window.select_prev()
        self.window_refresh()

    def cmd_next_page(self):
        self.window.select_next_page()
        self.window.refresh()

    def cmd_prev_page(self):
        self.window.select_prev_page()
        self.window.refresh()

    def cmd_home(self):
        self.window.select_first()
        self.window.refresh()

    def cmd_end(self):
        self.window.select_last()
        self.window.refresh()

    def cmd_enter(self):
        selected = self.window.get_selected()

        e = self.entries[selected]
        if self.is_directory(e):
            self.set_path(e.path, selected != 0)
        else:
            # TODO: Play track.
            pass

    def cmd_add(self):
        e = self.entries[self.window.get_selected()]

        if self.is_directory(e):
            plist = self.app.playlist
            self.app.client.add(plist.name, e)
        else:
            pass # TODO:

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
        self.list_win = window.ListWindow(self, 0, 1, self.width, self.height - 1)

        self.entries = []

    def activate(self):
        super().activate()

        self.path_win.activate()
        self.list_win.activate()

    def refresh(self):
        super().refresh()

        self.path_win.refresh()
        self.list_win.refresh()

    def set_path(self, path):
        self.path_win.erase()
        self.path_win.write(1, 0, path)

    def set_items(self, items):
        self.list_win.set_items(items)

    def get_selected(self):
        return self.list_win.get_selected()

    def set_selected(self, i):
        self.list_win.set_selected(i)

    def select_next(self):
        self.list_win.select_next()

    def select_prev(self):
        self.list_win.select_prev()

    def select_next_page(self):
        self.list_win.select_next_page()

    def select_prev_page(self):
        self.list_win.select_prev_page()

    def select_first(self):
        self.list_win.select_first()

    def select_last(self):
        self.list_win.select_last()
