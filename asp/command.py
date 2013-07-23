from acurses import key


GLOBAL = 'global'
BROWSER = 'browser'
PLAYLIST = 'playlist'


class Command:
    def __init__(self, name, description, keys):
        if not isinstance(keys, (list, tuple)):
            keys = (keys,)

        self.name = name
        self.description = description
        self.keys = keys

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

commands = {GLOBAL: [], BROWSER: [], PLAYLIST: []}


def register_cmd(var_name, controllers, name, descr, keys):
    if not isinstance(controllers, (list, tuple)):
        controllers = (controllers,)

    cmd = Command(name, descr, keys)

    # Define command name as package variable.
    g = globals()
    g[var_name] = cmd

    for c in controllers:
        commands[c].append(cmd)


def key_to_cmd(key, controller):
    for cmd in commands[controller]:
        if key in cmd.keys:
            return cmd

    return None


register_cmd('BACK', BROWSER, 'back', 'Go to parent directory', key.BACKSPACE)
register_cmd('DOWN', (BROWSER, PLAYLIST), 'down', 'Move cursor down', key.DOWN)
register_cmd('ENTER', BROWSER, 'enter', 'Enter into directory', key.ENTER)
register_cmd('SWITCH_WINDOW', GLOBAL, 'switch_window', 'Switch window', key.TAB)
register_cmd('UP', (BROWSER, PLAYLIST), 'up', 'Move cursor up', key.UP)
register_cmd('QUIT', GLOBAL, 'quit', 'Quit application', (key.q, key.Q))
