# -*- coding: utf-8 -*-

import socket


class BaseSocketTransport:

    def __init__(self, address):
        self.address = address
        self._socket = None
        self._opened = False

        self._buffer = None

    def send_request(self, call):
        self.ensure_open()
        self._socket.sendall(call.encode('ascii') + b'\n')
        return self._read_response()

    def close(self):
        if self._socket:
            self._socket.close()
            self._socket = None
            self._opened = False

    def _read_response(self):
        buf = b''
        while True:
            b = self._socket.recv(1)
            if b == b'\n':
                break
            buf += b

        return buf.decode('ascii')


class UnixDomainSocketTransport(BaseSocketTransport):

    def __init__(self, socket):
        super().__init__(socket)

    def ensure_open(self):
        if self._socket and self._opened:
            return

        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._socket.connect(self.address)
        self._opened = True


class TCPSocketTransport(BaseSocketTransport):

    def __init__(self, address, port):
        super().__init__((address, port))

    def ensure_open(self):
        if self._socket and self._opened:
            return

        self._socket = socket.create_connection(self.address)
        self._opened = True
