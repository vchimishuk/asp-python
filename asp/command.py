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


register_cmd('ADD', BROWSER, 'add',
             'Add track or directory to the current playlist',
             (key.a, key.A))
register_cmd('BACK', BROWSER, 'back',
             'Go to parent directory',
             key.BACKSPACE)
register_cmd('NEXT', (BROWSER, PLAYLIST),
             'next', 'Move to the next list item',
             key.DOWN)
register_cmd('END', (BROWSER, PLAYLIST),
             'end', 'Move to the last list item',
             (key.END, key.G))
register_cmd('ENTER', BROWSER,
             'enter', 'Enter into directory',
             key.ENTER)
register_cmd('HOME', (BROWSER, PLAYLIST),
             'home', 'Move to the first list item',
             key.HOME)
register_cmd('NEW_PLAYLIST', PLAYLIST,
             'new_playlist', 'Create new playlist',
             (key.n, key.N))
register_cmd('NEXT_PAGE', (BROWSER, PLAYLIST),
             'next_page', 'Move to the next page',
             key.PAGE_DOWN)
register_cmd('NEXT_PLAYLIST', PLAYLIST,
             'next_playlist', 'Switch to the next playlist',
             (key.l, key.L))
register_cmd('PREV_PAGE', (BROWSER, PLAYLIST),
             'prev_page', 'Move to the prevoius page',
             key.PAGE_UP)
register_cmd('PREV_PLAYLIST', PLAYLIST,
             'prev_playlist', 'Switch to the previous playlist',
             (key.h, key.H))
register_cmd('SWITCH_WINDOW', GLOBAL,
             'switch_window', 'Switch window',
             key.TAB)
register_cmd('PREV', (BROWSER, PLAYLIST),
             'prev', 'Move to the previous list item',
             key.UP)
register_cmd('QUIT', GLOBAL,
             'quit', 'Quit application',
             (key.q, key.Q))
