import curses
from gui import command
from gui import browser
from gui import playlist


class Controller:
    """
    Main controller dispatches user commands and delegates
    them to the concrete controller which is active at the moment.
    E.g. if browser window is active commands are sent to the browser
    controller.
    Some commands can be handled by main controller itself.
    """
    def __init__(self, client):
        self.client = client

        width = curses.LINES
        height = curses.COLS

        self.browser_window = browser.Window(width, height, 0, 0)
        self.browser_controller = browser.Controller(self.browser_window, client)
        self.browser_controller.set_path('/')

        self.playlist_window = playlist.Window(width, height, 0, 0)
        self.playlist_controller = playlist.Controller(self.playlist_window, client)

        self.current_controller = self.browser_controller
        self.current_controller.activate()

    def on_command(self, cmd):
        """
        Handle user input command.
        """
        if not self.handle_command(cmd):
            self.current_controller.on_command(cmd)

    def handle_command(self, cmd):
        """
        handle_command(command) -> bool
        Handle command which can be adressed to this controller.
        Returns True if command was handled completely and should not be
        propagated to the next level.
        """
        if cmd == command.CMD_QUIT:
            client.quit()
            # TODO: Exit not like english gentleman.
            import sys
            sys.exit(0)
        if cmd == command.CMD_TOGGLE_SCREEN:
            self.cmd_toggle_screen()
        else:
            return False

        return True

    def cmd_toggle_screen(self):
        """
        Rotate current screen.
        """
        if self.current_controller == self.browser_controller:
            self.current_controller = self.playlist_controller
        else:
            self.current_controller = self.browser_controller

        self.current_controller.activate()
