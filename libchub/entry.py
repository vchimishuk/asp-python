class Playlist:
    """
    Playlist model.
    """
    __slots__ = ['name', 'length']
    def __init__(self, name, length):
        self.name = mame
        self.length = length


class Directory:
    """
    Filesystem directory model.
    """
    __slots__ = ['name', 'path']
    
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        return '[{0}]'.format(self.name)


class Track:
    """
    Track filesystem or playlist entry model.
    """
    __slots__ = ['path', 'artist', 'album', 'title']
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.artist, self.album, self.title)
