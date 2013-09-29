class Entry:
    """
    Basic protocol object implemenation.
    """
    def __init__(self, d):
        """
        """
        for k, v in d.items():
            setattr(self, k.lower(), v)


class Playlist(Entry):
    """
    Playlist model.
    """
    __slots__ = 'name', 'length'

    def __str__(self):
        return self.name


class Directory(Entry):
    """
    Filesystem directory model.
    """
    __slots__ = 'name', 'path'

    def __str__(self):
        return '[{0}]'.format(self.name)


class Track(Entry):
    """
    Track filesystem or playlist entry model.
    """
    __slots__ = 'path', 'artist', 'album', 'title'

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.artist, self.album, self.title)
