import controller
import window
import command
import color


class Controller(controller.Controller):
    NAME = command.PLAYLIST

    def __init__(self, app, win):
        super().__init__(app, win)

        self.register_command(command.END, self.cmd_end)
        self.register_command(command.ENTER, self.cmd_enter)
        self.register_command(command.HOME, self.cmd_home)
        self.register_command(command.NEW_PLAYLIST, self.cmd_new_plist)
        self.register_command(command.NEXT, self.cmd_next)
        self.register_command(command.NEXT_PAGE, self.cmd_next_page)
        self.register_command(command.NEXT_PLAYLIST, self.cmd_next_plist)
        self.register_command(command.PREV, self.cmd_prev)
        self.register_command(command.PREV_PAGE, self.cmd_prev_page)
        self.register_command(command.PREV_PLAYLIST, self.cmd_prev_plist)

        self.selected = None
        self.plists_cache = {}
        self.load_plists()

    def load_plists(self):
        plists = self.app.client.playlists()

        self.set_plists(plists)
        self.set_plist(self.selected)

    def set_plists(self, plists, selected=None):
        if selected:
            self.selected = selected

        # Check if current playlist is stil exists.
        if self.selected:
            s = None
            for p in plists:
                if p.name == self.selected:
                    s = p.name
            self.selected = s

        # or select first one by default.
        if not self.selected and len(plists):
            self.selected = plists[0].name

        self.plists = plists

        l = []
        for p in plists:
            # TODO: Formatter.
            if p.name == self.selected:
                self.app.playlist = p
                l.append('[' + p.name + ']')
            else:
                l.append(p.name)

        self.window.set_plists(l)
        self.window_refresh()

    def set_plist(self, name):
        if name not in self.plists_cache:
            self.plists_cache[name] = self.app.client.playlist(name)

        self.window.set_tracks(self.plists_cache[name])
        self.window_refresh()

    def on_plists_changed(self):
        self.load_plists()

    def on_plist_changed(self, name):
        if name in self.plists_cache:
            del self.plists_cache[name]

        if name == self.selected:
            self.set_plist(name)

    def cmd_new_plist(self):
        name = self.prompt('Playlist name')
        if name:
            self.app.client.add_playlist(name)

    def cmd_next_plist(self):
        for i in range(len(self.plists) - 1):
            if self.plists[i].name == self.selected:
                selected = self.plists[i + 1].name
                self.set_plists(self.plists, selected)
                self.set_plist(selected)
                break

    def cmd_prev_plist(self):
        for i in range(1, len(self.plists)):
            if self.plists[i].name == self.selected:
                selected = self.plists[i - 1].name
                self.set_plists(self.plists, selected)
                self.set_plist(selected)
                break

    def cmd_next(self):
        self.window.select_next_track()
        self.window.refresh()

    def cmd_prev(self):
        self.window.select_prev_track()
        self.window.refresh()

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
        # TODO: Start playing selected track.
        pass


class Window(window.Window):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.tabs_win = self.subwin(0, 0, self.width, 1)
        self.tabs_win.set_background(color.PLAYLIST_TAB)
        self.list_win = window.ListWindow(self, 0, 1, self.width, self.height - 1)

    def refresh(self):
        super().refresh()

        self.tabs_win.refresh()
        self.list_win.refresh()

    def set_plists(self, plists):
        self.tabs_win.erase()

        titles = []
        for p in plists:
            titles.append(p)

        self.tabs_win.write(1, 0, ', '.join(titles))

    def set_tracks(self, tracks):
        self.list_win.set_items(tracks)

    def select_next_track(self):
        self.list_win.select_next()

    def select_prev_track(self):
        self.list_win.select_prev()

    def select_next_page(self):
        self.list_win.select_next_page()

    def select_prev_page(self):
        self.list_win.select_prev_page()

    def select_first(self):
        self.list_win.select_first()

    def select_last(self):
        self.list_win.select_last()
