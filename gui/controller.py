import curses
from gui import browser
from gui import command


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

        self.browser_window = browser.Window(curses.LINES, curses.COLS, 0, 0)
        self.browser_controller = browser.Controller(self.browser_window, client)
        self.browser_controller.set_path('/')

        self.default_controller = self.browser_controller

    def on_command(self, cmd):
        """
        Handle user input command.
        """
        if not self.handle_command(cmd):
            self.default_controller.on_command(cmd)

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
        else:
            return False

        return True
