import acurses
from acurses.color import BLACK, BLUE, CYAN, GREEN, MAGENTA, RED, WHITE, YELLOW


class Color:
    ID = 1

    def __init__(self, name, description, fg, bg):
        self.id = Color.ID
        Color.ID += 1

        self.name = name
        self.description = description
        self.fg = fg
        self.bg = bg

        self.update_pair()

    def update_pair(self):
        acurses.color.init_pair(self.id, self.fg, self.bg)
        self.color_pair = acurses.color.color_pair(self.id)

    @property
    def foreground(self):
        return self.fg

    @foreground.setter
    def foreground(self, c):
        self.fg = c
        self.update_pair()

    @property
    def background(self):
        return self.bg

    @background.setter
    def background(self, c):
        self.bg = c
        self.update_pair()

    @property
    def pair(self):
        return self.color_pair


BROWSER_PATH = Color('browser_path', 'Browser window path line',
                     BLACK, BLUE)
PLAYLIST_TAB = Color('playlist_tab', 'Playlist window tab',
                     BLACK, BLUE)
PLAYLIST_TAB_SELECTED = Color('playlist_tab_selected', 'Playlist window selected tab',
                              BLACK, RED)
STATUS_LINE = Color('status_line', 'Status line',
                    BLACK, BLUE)
LIST_SELECTED = Color('list_selected', 'Selected list item',
                      CYAN, BLACK)
