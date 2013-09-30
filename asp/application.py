import sys
from threading import Thread, Lock
from libchub import Client, NotificationClient, ConnectionError
import acurses
import command
import browser
import playlist
import prompt
import status


class NotificationThread(Thread):
    def __init__(self, client):
        super().__init__()

        self.daemon = True
        self.client = client

    def run(self):
        self.client.listen()


class Application:
    def synchronize(fn):
        """
        Protect public methods to be called from another threads.
        """
        def wrapper(app, *args, **kwargs):
            app.lock()
            fn(app, *args, **kwargs)
            app.unlock()

        return wrapper

    def __init__(self, stdscr, configs):
        # Curses initialization.
        stdscr.clear()
        acurses.echo(False)
        acurses.cbreak()
        acurses.cursor(False)
        stdscr.refresh()

        self.stdscr = stdscr

        # Server communication initialization.
        self.client = Client()
        self.notif_client = NotificationClient()
        self.notif_client.set_listener(NotificationClient.PLAYLISTS_CHANGED, self.on_playlists_changed)
        self.notif_client.set_listener(NotificationClient.PLAYLIST_CHANGED, self.on_playlist_changed)

        # TODO: Handle connection loose in a right way.
        try:
            self.client.connect(configs.host, configs.port)
            self.notif_client.connect(configs.host, configs.nport)
        except ConnectionError as e:
            print('Connection failed. ' + str(e))
            sys.exit(1)

        # Build the UI.
        height, width = self.stdscr.getmaxyx()

        # Creation of status (bottom screen) windows.
        win = status.Window(0, height - 2, width, 1)
        self.status_controller = status.Controller(win)

        win = prompt.Window(0, height - 1, width, 1)
        self.prompt_controller = prompt.Controller(win)

        # Creation of main windows.
        win = browser.Window(0, 0, width, height - 4)
        self.browser_controller = browser.Controller(self, win)
        self.browser_controller.set_path('/')
        win = playlist.Window(0, 0, width, height - 4)
        self.playlist_controller = playlist.Controller(self, win)
        self.playlist_controller.set_prompt_provider(self.prompt_controller.prompt)

        # Set active controller.
        self.controller = self.browser_controller
        self.controller.activate()

        # Start listening server's update notifications.
        self.notif_lock = Lock()
        self.notif_thread = NotificationThread(self.notif_client)
        self.notif_thread.start()

        self.command_handlers = {command.SWITCH_WINDOW: self.cmd_switch_window,
                                 command.QUIT: self.cmd_quit}

    @synchronize
    def on_playlists_changed(self, *args, **kwargs):
        self.playlist_controller.on_plists_changed(*args, **kwargs)

    @synchronize
    def on_playlist_changed(self, *args, **kwargs):
        self.playlist_controller.on_plist_changed(*args, **kwargs)

    def getch(self):
        return self.stdscr.getch()

    def run(self):
        while True:
            key = self.getch()
            self.lock()
            cmd = command.key_to_cmd(key, self.controller.NAME)

            # We should give a chance to handle the command to the
            # active controller. If it doesn't support that command the application
            # tries to handle it (aka global command).
            if cmd is None:
                cmd = command.key_to_cmd(key, command.GLOBAL)
                if cmd is not None:
                    self.on_command(cmd)
            else:
                if not self.controller.on_command(cmd):
                    self.on_command(cmd)

            self.unlock()

    def on_command(self, cmd):
        self.command_handlers[cmd]()

    def cmd_switch_window(self):
        if self.controller == self.browser_controller:
            self.controller = self.playlist_controller
            self.browser_controller.deactivate()
        else:
            self.controller = self.browser_controller
            self.playlist_controller.deactivate()

        self.controller.activate()

    def cmd_quit(self):
        # TODO: Normal exit process.
        raise Exception('quit')

    def lock(self):
        self.notif_lock.acquire()

    def unlock(self):
        self.notif_lock.release()
