from json import dumps, loads
from random import choice, randint
from requests import get, post, session
from .errors import *
from .crypto import Encryption
from .storage import SQLiteSession
from .clients import *
import typing

class Errors:
    
    def MadeError(status: str, det: str) -> (bool):

        if status.upper() == 'ERROR_GENERIC' or status.upper() == 'ERROR_ACTION':
            if 'NOT_REGISTERED' in det.upper():
                raise NotREGISTERED('session key not found; please find your key in web.rubika.ir and try again.')
            elif 'INVALID_INPUT' in det.upper():
                raise InvalidInput('your inserts is not true; try again.')
            elif 'TOO_REQUESTS' in det.upper():
                raise TooREQUESTS('sorry: method has been limited, please try again later.')
            elif 'INVALID_AUTH' in det.upper():
                raise InvalidAUTH('sorry: server error or please check method arguments and try again.')
            else:
                return True
        else:
            return True

class ClientConnectorError(object):
    
    @classmethod
    def __init__(cls, **kwargs: object) -> (...):
        cls.set_error: ConnectError = kwargs.get('error')
        cls.name: str = kwargs.get('name')
        super().__init__(cls.name, cls.set_error)
        
    @property
    def raises(cls) -> (Exception):
        raise cls.set_error(f'this error for {cls.name}')
    
    @property
    def returns(cls) -> (str):
        return 'this error for %s please fixed and try again.' %  cls.name

class Urls(str):
    
    def get_url() -> (str):
        
        for i in range(3):
            try:
                return choice(list(loads(__import__('urllib').request.urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('API').values()))
            except Exception:
                continue

    giveUrl = lambda mode, key=None: SQLiteSession(key).information()[3] if key and 'https://' in SQLiteSession(key).information() else ('https://messengerg2c{}.iranlms.ir/'.format(str('56' if mode.lower() == 'mashhad' else '74' if mode.lower() == 'tehran' else str(randint(3, 74)))))

class Make(object):
    
    def evolution(message, key) -> (dict):
        
        res: dict = {}
        
        try:
            res: dict = loads(Encryption(key).decrypt(message.get('data_enc')))
        except Exception:
            ...

        if Errors.MadeError(res.get('status') or '', res.get('status_det') or ''):
            return res

class Connection(dict):

    timeout: int = 5

    @staticmethod
    def postion(
        url     :   (str),
        data    :   (dict),
        proxy   :   (dict),
        auth    :   (str),
        mode    :   (bool) = (False)
        ) -> (
            dict
            ):

            
            with session() as (sent):

                for (i) in range(3):
                    
                    try:
                        
                        return (Make.evolution((sent).post(url, json=(data) if not mode else dumps(data), timeout=Connection.timeout, proxies=proxy).json(), (auth)))
                    
                    except Exception as e:
                        if i >= 2:
                            raise e
                    finally:
                        pass

                else:
                    raise ServerError('`sorry`: device can\'t connect to the server and is not response, please checked your network.')

class GetData(Connection):
    
    url: typing.Union[str, bool] = False
    
    @staticmethod
    def api(
        **kwargs
        ) -> (typing.Union[dict, Connection]):

        '''
        # API METHODS
        
        ## EXAMPLE:
        
            - `version` =   '5' or '4',
            - `auth`    =   'key',
            - `tmp`     =   ...
            - `method`  =   'methodName'
            - `data`    =   input,
            - `mode`    =  'mashhad',
            - `platform`=   'rubx' or 'web',
            - `proxy`   =   {'https':'127.0.0.1:9050'} # a dictionary type
        '''

        main: list = []
        
        if (kwargs.get('version') == '5'):
            main.extend(
                [
                    {
                        'api_version'   :   '5',
                        '{}'.format('auth' if kwargs.get('auth') else 'tmp_session') :   kwargs.get('auth') or kwargs.get('tmp'),
                        'data_enc'      :  dumps({'input': kwargs.get('data'), 'client': clients.web if kwargs.get('platform') == 'web' else clients.rubx, 'method': kwargs.get('method')}) if not kwargs.get('auth') else Encryption(kwargs.get('auth')).encrypt(dumps({'input': kwargs.get('data'), 'client': clients.web if kwargs.get('platform') == 'web' else clients.rubx, 'method': kwargs.get('method')}))
                        }
                    ]
                )
        
        else:
            main.extend(
                [
                    {
                        'api_version'   :   '4',
                        'auth'          :   kwargs.get('auth'),
                        'client'        :   clients.android,
                        'method'        :   kwargs.get('method'),
                        'data_enc'      :   Encryption(kwargs.get('auth')).encrypt(dumps(kwargs.get('data')))
                }
                    ]
                )

        return (Connection.postion(GetData.url or Urls.giveUrl(kwargs.get('mode'), kwargs.get('auth') or kwargs.get('tmp_session')), main[0], kwargs.get('proxy'), kwargs.get('auth') or kwargs.get('tmp_session')))