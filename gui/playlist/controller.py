from gui.basecontroller import BaseController


class Controller(BaseController):
    """
    Playlists screen controller.
    """
    def __init__(self, window, client):
        super().__init__(window)

        self.client = client

        self.set_playlists(self.client.playlists())

    def set_playlists(self, plists):
        """
        Set available playlists list.
        """
        l = []
        for p in plists:
            # TODO: Formatter.
            l.append('{0} ({1})'.format(p.name, p.length))

        self.window.set_playlists(l)
        self.window.refresh()
