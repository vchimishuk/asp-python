class BaseController:
    """
    Basic controller implementation.
    """
    def __init__(self):
        self.command_handlers = {}

    def register_command(self, cmd, handler):
        self.command_handlers[cmd] = handler

    def on_command(self, cmd):
        if cmd in self.command_handlers:
            self.command_handlers[cmd]()
