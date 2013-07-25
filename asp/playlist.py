import controller
import window
import command
import color


class Controller(controller.Controller):
    NAME = command.PLAYLIST

    def __init__(self, win, client):
        super().__init__(win)

        self.client = client

        self.register_command(command.DOWN, self.cmd_down)
        self.register_command(command.ENTER, self.cmd_enter)
        self.register_command(command.NEW_PLAYLIST, self.cmd_new_playlist)
        self.register_command(command.UP, self.cmd_up)

        self.set_playlists(self.client.playlists())

    def set_playlists(self, plists):
        l = []
        for p in plists:
            # TODO: Formatter.
            l.append('{0} ({1})'.format(p.name, p.length))

        self.window.set_playlists(l)

    def cmd_down(self):
        pass

    def cmd_enter(self):
        pass

    def cmd_new_playlist(self):
        name = self.prompt('Playlist name')
        self.client.add_playlist(name)

    def cmd_up(self):
        pass


class Window(window.Window):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.tabs_win = self.subwin(0, 0, self.width, 1)
        self.tabs_win.set_background(color.PLAYLIST_TAB)
        self.list_win = self.subwin(0, 1, self.width, self.height - 1)

    def refresh(self):
        super().refresh()

        self.tabs_win.refresh()
        self.list_win.refresh()

    def set_playlists(self, plists):
        self.tabs_win.erase()

        titles = []
        for p in plists:
            titles.append(p)

        self.tabs_win.write(1, 0, ', '.join(titles))
        self.refresh()
