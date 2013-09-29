import socket


class TextSocket(socket.socket):
    """
    TextSocket extends standard Python socket with some helper
    methods for working with text strings.
    """
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, *args, **kwargs):
        super().connect(*args, **kwargs)
        self.fileobject = self.makefile(mode='rw')

    def write(self, s):
        """
        write_line() -> None
        Writes given string to the socket and appends \n at the end.
        """
        self.fileobject.write(s)
        if s.endswith('\n'):
            self.fileobject.flush()

    def readline(self):
        """
        read_line() -> line
        Reads one line. Result line doesn't includes new line character
        at the end.
        """
        return self.fileobject.readline().strip()
