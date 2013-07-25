import sys
import libchub
import acurses
import command
import browser
import playlist
import prompt


class Application:
    def __init__(self, stdscr):
        stdscr.clear()
        acurses.echo(False)
        acurses.cbreak()
        acurses.cursor(False)
        stdscr.refresh()

        self.stdscr = stdscr
        self.client = libchub.Client()

        self.command_handlers = {command.SWITCH_WINDOW: self.cmd_switch_window,
                                 command.QUIT: self.cmd_quit}

        # TODO: Handle connection loose in a right way.
        try:
            self.client.connect("localhost", 1488)
        except libchub.ConnectionError as e:
            print('Connection failed. ' + str(e))
            sys.exit(1)

        height, width = self.stdscr.getmaxyx()

        # Creation of status (bottom screen) windows.
        win = prompt.Window(0, height - 1, width, 1)
        self.prompt_controller = prompt.Controller(win)
        self.prompt_controller.activate()
        
        # Creation of main windows.
        win = browser.Window(0, 0, width, height - 4)
        self.browser_controller = browser.Controller(win, self.client)
        self.browser_controller.set_path('/')
        win = playlist.Window(0, 0, width, height - 4)
        self.playlist_controller = playlist.Controller(win, self.client)
        self.playlist_controller.set_prompt_provider(self.prompt_controller.prompt)

        # Set active controller.
        self.controller = self.browser_controller
        self.controller.activate()

    def getch(self):
        return self.stdscr.getch()

    def run(self):
        while True:
            key = self.getch()
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

    def on_command(self, cmd):
        self.command_handlers[cmd]()

    def cmd_switch_window(self):
        if self.controller == self.browser_controller:
            self.controller = self.playlist_controller
        else:
            self.controller = self.browser_controller
    
        self.controller.activate()

    def cmd_quit(self):
        # TODO: Normal exit process.
        raise Exception('quit')
