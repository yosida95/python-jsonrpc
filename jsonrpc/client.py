# -*- coding: utf-8 -*-

import json
import uuid

__all__ = ['ServerProxy', 'Call']


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


class Response:

    def __init__(self, call, response):
        self.call = call
        self.response = response

    def get_result(self):
        if self.has_error():
            return None
        return self.response.get('result')

    def get_error(self):
        return self.response.get('error')

    def has_error(self):
        return self.get_error() is not None


class ServerProxy:

    version = '2.0'
    response_cls = Response

    def __init__(self, uri, transport):
        self.uri = uri
        self.transport = transport

    def send_request(self, call):
        encoded = json.dumps(call)
        resp = self.transport.send_request(encoded)

        respobj = json.loads(resp)
        if not isinstance(respobj, dict):
            raise ValueError()

        return self.response_cls(call, respobj)

    def __getattr__(self, name):
        return Call(name, self.version, self.send_request)

    def close(self):
        if self.transport:
            self.transport.close()
