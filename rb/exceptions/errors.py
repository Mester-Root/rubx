#!/bin/python

class SessionError(OSError):
    pass

class MainError(Exception):
    pass

class NotREGISTERED(IOError):
    pass

class InvalidInput(IOError):
    pass

class TooREQUESTS(IOError):
    pass

class InvalidAUTH(IOError):
    pass

class ConnectError(OSError):
    pass

class ClientError(Exception):
    pass

class ServerError(Exception):
    pass

class ApiHasNotResponse(Exception):
    pass

class APIError(Exception):
    pass

class BotApiTimeOutError(Exception):
    pass

__all__ = ['SessionError', 'MainError', 'NotREGISTERED',
           'InvalidInput', 'TooREQUESTS', 'InvalidAUTH',
           'ConnectError', 'ClientError', 'ServerError',
           'APIError', 'BotApiTimeOutError', 'ApiHasNotResponse']