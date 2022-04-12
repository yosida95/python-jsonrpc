# -*- coding: utf-8 -*-

import socket


class BaseSocketTransport:
    _DEFAULT_TIMEOUT = object()

    def __init__(self, address, response_encoding, timeout=_DEFAULT_TIMEOUT):
        self.address = address
        self._socket = None
        self._rfile = None
        self._response_encoding = response_encoding
        self._timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_info, exc_value, traceback):
        self.close()
        return False

    def send_request(self, call):
        self.ensure_open()
        self._socket.sendall(call.encode('ascii') + b'\n')
        return self._read_response()

    def ensure_open(self):
        raise NotImplementedError()

    def close(self):
        if self._rfile:
            self._rfile.close()
            self._rfile = None
        if self._socket:
            self._socket.close()
            self._socket = None

    def _read_response(self):
        if self._rfile is None:
            self._rfile = self._socket.makefile(
                'r', encoding=self._response_encoding)
        try:
            buf = self._rfile.readline()
        except socket.timeout:
            self.close()
            raise
        if buf == '':
            self.close()
            raise OSError('socket closed')
        return buf.strip()


class UnixDomainSocketTransport(BaseSocketTransport):

    def __init__(
        self, socket, response_encoding='ascii',
        timeout=BaseSocketTransport._DEFAULT_TIMEOUT
    ):
        super().__init__(
            address=socket, response_encoding=response_encoding,
            timeout=timeout)

    def ensure_open(self):
        if self._socket:
            return
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if self._timeout is not self._DEFAULT_TIMEOUT:
            s.settimeout(self._timeout)
        s.connect(self.address)
        self._socket = s


class TCPSocketTransport(BaseSocketTransport):

    def __init__(
        self, address, port, response_encoding='ascii',
        timeout=BaseSocketTransport._DEFAULT_TIMEOUT,
    ):
        super().__init__(
            address=(address, port), response_encoding=response_encoding,
            timeout=timeout)

    def ensure_open(self):
        if self._socket:
            return

        if self._timeout is self._DEFAULT_TIMEOUT:
            self._socket = socket.create_connection(self.address)
        else:
            self._socket = socket.create_connection(
                self.address, timeout=self._timeout)
