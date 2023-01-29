#!/bin/python

from json           import  dumps, loads, dump, load, JSONDecodeError
from random         import  choice, randint
from requests       import  get, post, session
from .exceptions    import  *
from .crypto        import  Encryption
from .storage       import  SQLiteSession
from .clients       import  *
import typing, re


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
    def __init__(cls, **kwargs) -> None:
        
        '''
        class StorageError(OSError): pass
        
        error = ClientConnectorError(name='[StorageError] dont access to your device.', error=StorageError)
        
        print(error.returns)
        error.warnings
        error.raises
        '''
        
        cls.set_error, cls.name = kwargs.get('error'), kwargs.get('name')

    @property
    def raises(cls) -> (Exception):
        raise cls.set_error(f'this error for {cls.name}')
    
    @property
    def returns(cls) -> (str):
        return 'this error for %s please fixed and try again.' %  cls.name

    @property
    def warnings(cls) -> (str):
        __import__('warnings').warn(cls.name)


class Urls(str):
    
    def get_url() -> (str):
        
        for i in range(3):
            try:
                return choice(list(loads(__import__('urllib').request.urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('API').values()))
            except Exception:
                continue

    giveUrl = lambda mode, key=None: SQLiteSession(key).information()[3] if key and 'https://' in SQLiteSession(key).information() else ('https://messengerg2c{}.iranlms.ir/'.format(str('56' if mode.lower() == 'mashhad' else '74' if mode.lower() == 'tehran' else str(randint(3, 74)))))


class MakeDataKeys(object):

    def __str__(self) -> (str):
        return dumps(
            self.result_data,
            indent=4,
            ensure_ascii=False,
            default=str
            )

    def __getattr__(self, name) -> (list):
        return self.keys_finder(keys=name)

    def __setitem__(self, key, value) -> (None):
        self.result_data[key] = value

    def __getitem__(self, key):
        return self.result_data[key]

    def __lts__(self, update: list) -> (list):
        
        for index, element in enumerate(update):
            if isinstance(element, list):
                update[index] = self.__lts__(update=element)

            elif isinstance(element, dict):
                update[index] = MakeDataKeys(update=element)

            else:
                update[index] = element
        return update

    def __init__(self, update: dict = None) -> (None):
        
        '''
        # this object for get keys from a dictionary
        
        `result.data.chat`
        `result.get('data').get('chat')`
        
        '''
        
        self.result_data = update

    def keys_finder(self, keys: list,
                  result_data: str = None) -> (list):

        if not result_data:
            result_data = self.result_data

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(result_data, dict):
            for key in keys:
                try:
                    update = result_data[key]
                    if isinstance(update, dict):
                        update = MakeDataKeys(update=update)

                    elif isinstance(update, list):
                        update = self.__lts__(update=update)

                    return update

                except KeyError:
                    pass
            result_data = result_data.values()

        for value in result_data:
            if isinstance(value, (dict, list)):
                try:
                    return self.keys_finder(keys=keys, result_data=value)

                except AttributeError:
                    pass
        else:
            ClientConnectorError(name='data has not (%s) key' % ', '.join(keys), error=KeyError).raises


class Make(object):

    action: str = 'dict'

    def evolution(message, key) -> (dict):
        
        res: dict = {}
        
        try:
            res: dict = loads(Encryption(key).decrypt(message.get('data_enc')))
        except Exception:
            ...

        if Errors.MadeError(res.get('status') or '', res.get('status_det') or ''):
            return (res) if not Make.action == 'str' else MakeDataKeys(res)


class Connection(dict):

    timeout, headers, api_version, platform, action = 5, None, '5', 'web', 'sync'
    # TODO: the set all variable to params from init object and dont use on methods func.
    
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
                        if Connection.action == 'async':
                            pass
                        else:
                            return (Make.evolution((sent).post(url, json=(data) if not mode else dumps(data), timeout=Connection.timeout, proxies=proxy).json(), (auth)))
                    
                    except Exception as e:
                        if i >= 2 and not JSONDecodeError in i:
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
