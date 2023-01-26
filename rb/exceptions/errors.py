#!/bin/python

class Exceptions:
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