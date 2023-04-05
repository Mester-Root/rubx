#!/bin/python

from json import loads, dumps
from random import choice
from .crypto import Encryption

class WebSocket(object):

    def __init__(self, session, action: bool = False) -> (None):
        self.auth, self.action = session, action
        self.enc: Encryption = Encryption(session)

    def __enter__(self) -> (object):
        return self

    def __exit__(self, *args, 
                 **kwargs) -> (None):
        pass

    def __on_open(self, ws, api_version='4') -> (None):
        ws.send(dumps({'api_version': api_version, 'auth': self.auth, 'method': 'handShake'}))
    
    def __on_send(self, ws) -> (None):
        ws.send(dumps({}))

    def __on_message(self, message) -> (dict):
        
        try:

            parsedMessage: dict = loads(message)
            return {'type': parsedMessage.get('type') or 'messenger', 'data': loads(self.enc.decrypt(parsedMessage.get('data_enc')))}

        except Exception:
            return {'type': '', 'data': ''}

    def __connector(self, ws: object, mode: str = '1') -> (None):
        try:
            if mode.__eq__('1'):
                self.__on_open(ws, '4')
            else:
                self.__on_send(ws)
        except Exception:
            pass
    
    @property
    def connection(self) -> (None):

        '''
        async with __import__('websockets').connect('wss://jsocket4.iranlms.ir:80') as ws:
            ... # TODO: use the async websocket client
        '''

        from websocket import create_connection

        ws, count = create_connection(choice(['wss://jsocket4.iranlms.ir:80', 'wss://nsocket9.iranlms.ir:80/', 'wss://nsocket1.iranlms.ir:80/'])), 0
        self.__connector(ws)
        
        if self.action:
            return ws.recv()

        while 1:

            try:
                for res in [ws.recv()]:
                    
                    count: int = count.__add__(1)

                    if ((count / 2).__round__()).__eq__(40): # 80
                        self.__connector(ws, '2')

                    elif ((count / 2).__round__()).__eq__(60): # 120
                        self.__connector(ws, '1')
                        count: int = 0

                    if str(res).__len__().__ne__(33):
                        yield self.__on_message(res)

            except Exception:
                pass