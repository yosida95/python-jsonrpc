# -*- coding: utf-8 -*-

import json
import uuid

__all__ = ['ServerProxy', 'Call', 'Error']


class Call:

    def __init__(self, method, version, caller=None):
        self.method = method
        self.version = version
        self.caller = caller

    def _generate_id(self):
        return str(uuid.uuid4())

    def set_caller(self, caller):
        self.caller = caller

    def dump(self, params):
        if self.version == '2.0':
            dct = dict(jsonrpc=self.version,
                       method=self.method,
                       id=self._generate_id())

            if params:
                dct.update(params=params)

            return dct

        raise NotImplementedError()

    def __getattr__(self, name):
        return Call(self.method + '.' + name, self.version, self.caller)

    def __call__(self, *args, **kwargs):
        if len(args) == len(kwargs) == 0:
            params = dict()
        elif len(args) == 0:
            params = kwargs
        elif len(kwargs) == 0:
            params = args
        else:
            raise ValueError('All parameters must be anonymouse or named')

        return self.caller(self.dump(params))


class Error(Exception):

    def __init__(self, code, message=None, data=None):
        self.code = code
        self.message = message
        self.data = data

    def __repr__(self):
        return '<Error[{code!d}] at 0x{id!x}>'.format(code=self.code,
                                                      id=id(self))


class ServerProxy:

    version = '2.0'
    error_cls = Error

    def __init__(self, transport):
        self.transport = transport

    def send_request(self, call):
        encoded = json.dumps(call)
        resp = self.transport.send_request(encoded)
        ParseError = self.error_cls(-32700, 'Parse error')
        InternalError = self.error_cls(-32603, 'Internal error')

        try:
            respobj = json.loads(resp)
        except ValueError as why:
            raise ParseError from why

        if not isinstance(respobj, dict):
            raise ParseError

        try:
            if respobj['id'] != call['id']:
                raise InternalError

            error = respobj.get('error')
            if error:
                if not isinstance(error, dict):
                    raise ParseError
                raise self.error_cls(error['code'],
                                     error.get('message'),
                                     error.get('dta'))

            return respobj['result']
        except KeyError as why:
            raise ParseError from why

    def __getattr__(self, name):
        return Call(name, self.version, self.send_request)

    def close(self):
        if self.transport:
            self.transport.close()
