import socket
import itertools
from collections import defaultdict
from libchub.textsocket import TextSocket
from libchub.entry import Playlist, Directory, Track


class ConnectionError(Exception):
    """
    ConnectionException raised on any communication problems with server.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ProtocolError(Exception):
    """
    ProtocolError exception raises by public Client methods when
    server response with ERR on some particular command.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TextProtocolClient:
    def __init__(self):
        self.sock = TextSocket()

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            raise ConnectionError(e.strerror)

    def write_command(self, cmd, *args):
        """
        write_command() -> None
        Send command to the server.
        """
        self.sock.write(cmd)
        if len(args):
            self.sock.write(' ')
        self.sock.write(' '.join(['"' + a + '"' for a in args]))
        self.sock.write('\n')

    def parse_dict(self, line):
        """
        parse_dict(line) -> dict
        parse_dict parses protocol key-value line to dict.
        """
        try:
            return parse_dict(line)
        except ValueError as e:
            raise ProtocolError('Failed to parse server response.' + str(e))

    def read_response(self):
        """
        read_response() -> [response lines]
        bool return value indicates is server responsed with OK or ERROR status.
        """
        status = self.sock.readline()
        lines = []

        while True:
            s = self.sock.readline()

            if s:
                lines.append(s)
            else:
                break

        if status == Client.STATUS_OK:
            return lines
        elif not len(status):
            raise ConnectionError('Server connection is dead')
        else:
            raise ProtocolError(' '.join(lines))


# TODO: Add debug logging.
class Client(TextProtocolClient):
    STATUS_OK = "OK"
    STATUS_ERR = "ERR"

    ENTRY_TYPE_DIR = 'DIRECTORY'
    ENTRY_TYPE_TRACK = 'TRACK'

    CMD_ADD = 'ADD'
    CMD_ADD_PLAYLIST = 'ADDPLAYLIST'
    CMD_LS = 'LS'
    CMD_PING = 'PING'
    CMD_PLAYLIST = 'PLAYLIST'
    CMD_PLAYLISTS = 'PLAYLISTS'
    CMD_QUIT = 'QUIT'

    """
    Chub client protocol implementation.
    """
    def connect(self, *args, **kwargs):
        super().connect(*args, **kwargs)

        # Read server's greetings.
        try:
            self.read_response()
        except ProtocolError as e:
            raise ConnectionError('Server greetings failed. ' + e.msg)


    def add(self, playlist, entry):
        """
        add(playlist name, Directory or Track) -> None
        Add directory or track to the current playlist.
        """
        self.write_command(Client.CMD_ADD, playlist, entry.path)
        self.read_response()

    def add_playlist(self, name):
        """
        add_playlist(name) -> None
        Create new playlist with given name.
        """
        self.write_command(Client.CMD_ADD_PLAYLIST, name)
        self.read_response()

    def ls(self, path):
        """
        ls() -> list of tracks and folders in the current directory.
        """
        self.write_command(Client.CMD_LS, path)

        entries = []
        for l in self.read_response():
            d = self.parse_dict(l)
            if d['Type'] == Client.ENTRY_TYPE_DIR:
                e = Directory(d)
            else:
                e = Track(d)

            entries.append(e)

        return entries

    def ping(self):
        """
        ping() -> None
        Send PING command. PING command do nothing, just pings
        server and reveives simple OK answer.
        """
        self.write_command(Client.CMD_PING)
        self.read_response()

    def playlists(self):
        """
        playlists() -> [Playlist]
        Returns playlists list.
        """
        self.write_command(Client.CMD_PLAYLISTS)

        plists = []
        for l in self.read_response():
            plists.append(Playlist(self.parse_dict(l)))

        return plists

    def playlist(self, name):
        """
        playlist(name) -> [track]
        Returns tracks list in the playlist.
        """
        self.write_command(Client.CMD_PLAYLIST, name)

        tracks = []
        for l in self.read_response():
            tracks.append(Track(self.parse_dict(l)))

        return tracks

    def quit(self):
        """
        quit() -> None
        quit sends QUIT command and closes connection with server.
        """
        self.write_command(Client.CMD_QUIT)
        self.read_response()
        self.sock.close()


class NotificationClient(TextProtocolClient):
    PLAYLIST_CHANGED = 'PLAYLIST_CHANGED'
    PLAYLISTS_CHANGED = 'PLAYLISTS_CHANGED'
    STATE_CHANGED = 'STATE_CHANGED'
    TRACK_CHANGED = 'TRACK_CHANGED'
    VOLUME_CHANGED = 'VOLUME_CHANGED'

    def __init__(self):
        super().__init__()

        self.listeners = defaultdict(list)

    def set_listener(self, event, callback):
        """
        Set event listener.
        """
        self.listeners[event].append(callback)

    def remove_listener(self, event, callback):
        """
        Disable listener.
        """
        self.listeners[event].remove(callback)

    def listen(self):
        """
        Start listening for notifications.
        """
        while True:
            line = self.sock.readline()

            if not len(line):
                raise ConnectionError('Server connection is dead')

            p = line.split(' ', 1)
            event = p[0]

            if len(p) > 1:
                # TODO: Now supported only one parameter. Split values.
                #args = [parse_val(v) for v in p[1]]
                args = [parse_val(p[1])]
            else:
                args = []

            for listener in self.listeners[event]:
                listener(*args)


def split_pairs(line):
    """
    split_pairs(line) -> [pair string]
    Split server response line into key-value pairs.
    """
    pairs = []
    s = ''
    quote_mode = False
    esc_mode = False

    for c in itertools.chain(line, ","):
        if not esc_mode and not quote_mode and c == ',':
            pairs.append(s.strip())
            s = ''
        elif esc_mode:
            s += '\\' + c
            esc_mode = False
        elif c == '\\':
            esc_mode = True
        elif c == '"':
            quote_mode = not quote_mode
            s += c
        else:
            s += c

    if quote_mode or esc_mode:
        raise ValueError('Bad protocol line format.')

    return pairs


def parse_val(v):
    """
    parse_val(raw_value) -> str or int
    """
    if v.startswith('"'):
        v = v.strip('"')
        v = v.replace('\\\\', '\\')
        v = v.replace('\\n', '\n')
        v = v.replace('\\"', '\"')
        v = v.replace('\\\'', '\'')
    else:
        v = int(v)

    return v

def parse_dict(line):
    """
    parse_dict(line) -> dict
    Parses server response line to dict.
    """
    res = {}

    pairs = split_pairs(line)
    for pair in pairs:
        k, v = [s.strip() for s in pair.split(':', 1)]
        res[k] = parse_val(v)

    return res
