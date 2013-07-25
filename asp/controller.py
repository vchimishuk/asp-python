class Controller:
    """
    Main window (browser, playlist, etc) basic controller implementation.
    """

    # Must be defined in childs.
    NAME = 'NONE'

    """
    Basic controller implementation.
    """
    def __init__(self, window):
        self.window = window
        self.command_handlers = {}

    def register_command(self, cmd, handler):
        self.command_handlers[cmd] = handler

    def on_command(self, cmd):
        """
        on_command(cmd) -> bool
        Process user input command and returns True if it was completely
        processed by this controller. False return value means that this
        command is not supported by this controller and should be handled
        by main application controller.
        """
        handler = self.command_handlers.get(cmd, None)
        if handler:
            handler()

            return True
        else:
            return False

    def refresh_window(self):
        self.window.refresh()

    def activate(self):
        """
        Brings this controller to top, which mean it will receives user's input
        and its screen will be visible.
        """
        self.window.top()
        self.window.refresh()

    def set_prompt_provider(self, provider):
        """
        Set prompt provider function.
        provider function can be called with prompt string argument
        to receive some user input.
        """
        self.prompt_provider = provider

    def prompt(self, ps):
        """
        Ask user for some string value to input.
        """
        return self.prompt_provider(ps)


class StatusController:
    """
    Status window (prompt, status) base controller implementation.
    """
    def __init__(self, win):
        self.window = win

    def activate(self):
        self.window.top()
        self.window.refresh()
