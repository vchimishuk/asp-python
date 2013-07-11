import curses


# User input commands.
CMD_BACK = 0x01
CMD_DOWN = 0x02
CMD_ENTER = 0x03
CMD_RESIZE = 0x04
CMD_UP = 0x05
CMD_QUIT = 0x06


cmd_mapping = {10: CMD_ENTER,
               curses.KEY_BACKSPACE: CMD_BACK,
               curses.KEY_DOWN: CMD_DOWN,
               curses.KEY_ENTER: CMD_ENTER,
               curses.KEY_RESIZE: CMD_RESIZE,
               curses.KEY_UP: CMD_UP,
               ord('q'): CMD_QUIT}


def translate_curses_key(key):
    return cmd_mapping.get(key, None)
