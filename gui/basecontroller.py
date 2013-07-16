class BaseController:
    """
    Basic controller implementation.
    """
    def __init__(self, window):
        self.window = window
        self.command_handlers = {}

    def register_command(self, cmd, handler):
        self.command_handlers[cmd] = handler

    def on_command(self, cmd):
        if cmd in self.command_handlers:
            self.command_handlers[cmd]()

    def refresh_window(self):
        self.window.refresh()

    def activate(self):
        """
        Brings this controller to top, which mean it will receives user's input
        and its screen will be visible.
        """
        self.window.activate()
        self.window.refresh()
