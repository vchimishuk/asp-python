import socket
import itertools
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


# TODO: Add debug logging.
class Client:
    STATUS_OK = "OK"
    STATUS_ERR = "ERR"

    ENTRY_TYPE_DIR = 'DIRECTORY'
    ENTRY_TYPE_TRACK = 'TRACK'

    # TODO: Test bad command name error.
    CMD_ADD_PLAYLIST = 'ADDPLAYLIST'
    CMD_LS = 'LS'
    CMD_PING = 'PING'
    CMD_PLAYLISTS = 'PLAYLISTS'
    CMD_QUIT = 'QUIT'
    
    """
    Chub client protocol implementation.
    """
    def __init__(self):
        self.sock = TextSocket()

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            raise ConnectionError(e.strerror)

        # Read server's greetings.
        try:
            self.read_response()
        except ProtocolError as e:
            raise ConnectionError('Server greetings failed. ' + e.msg)

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
                e = Directory(d['Name'], d['Path'])
            else:
                e = Track(artist=d['Artist'], album=d['Album'], title=d['Title'])

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
            d = self.parse_dict(l)
            plists.append(Playlist(d['Name'], int(d['Length'])))

        return plists

    def quit(self):
        """
        quit() -> None
        quit sends QUIT command and closes connection with server.
        """
        self.write_command(Client.CMD_QUIT)
        self.read_response()

    def read_response(self):
        """
        read_response() -> [response lines]
        bool return value indicates is server responsed with OK or ERROR status.
        """
        status = self.sock.readline().strip()
        lines = []
    
        while True:
            s = self.sock.readline().strip()

            if s:
                lines.append(s)
            else:
                break

        if status == Client.STATUS_OK:
            return lines
        else:
            raise ProtocolError(' '.join(lines))

    def write_command(self, cmd, *args):
        """
        write_command() -> None
        Send command to the server.
        """
        self.sock.write(cmd)
        if len(args):
            self.sock.write(' ')
        # TODO: Escape string args if needed only.
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


def parse_dict(line):
    """
    parse_dict(line) -> dict
    Parses server response line to dict.
    """
    res = {}    
    
    pairs = split_pairs(line)
    for pair in pairs:
        k, v = [s.strip() for s in pair.split(':', 1)]

        # Conver v from string literal to Python string.
        v = v.strip('"')
        v = v.replace('\\\\', '\\')
        v = v.replace('\\n', '\n')
        v = v.replace('\\"', '\"')
        v = v.replace('\\\'', '\'')

        res[k] = v

    return res
