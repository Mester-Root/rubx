#!/bin/python

from os import path

if __name__ == '__main__' and  __package__ == None or __package__ == '':
    __import__('sys').path.append(path.join(path.dirname(__file__), '..'))

import logging
import platform
import sqlite3
import typing
import webbrowser
from base64 import b64encode, urlsafe_b64decode
from datetime import datetime
from json import dumps, loads
from os import system
from pathlib import Path
from random import choice, randint, sample
from re import compile
from re import findall, search, sub
from time import sleep
from warnings import warn

from Crypto.Cipher.AES import (MODE_CBC,
                               block_size, new)
from Crypto.Util.Padding import pad, unpad
from requests import get, post, session

if typing.TYPE_CHECKING:
    from . import StartClient, UserMethods

try:
    from . import __file__ as base_file
    from . import __name__ as base_log
    from . import __package__ as base_pkg

except ImportError:
    base_file, base_log, base_pkg = locals().get('__file__') or __doc__, locals().get('__name__'), locals().get('__package__')

__all__ = [
    'Client',
    'StartClient',
    'RubinoClient',
    'WebSocket',
    'Handler',
    'NewMessage',
    'EventBuilder',
    'UserMethods',
    'GroupMethods',
    'ChannelMethods',
    'UpToDate',
    'Version'
    ]

class Version(str):
    __version__ =   '10.1.9'
    __author__  =   'saleh'
    __lisense__ =   'MIT'

__version__ = Version.__version__

class __Top(object):
    
    @classmethod
    def __init__(cls, session: str) -> (None):
        cls.session = session
    
    def __detecting(cls) -> (dict):

        if isinstance(cls.session, str) and len(cls.session) == 32:
            exits, session, add, index = False, [*cls.session], '', []
            for key, n in zip(cls.session, range(len(cls.session))):
                if session.count(key) >= 2:
                    add += key
                    index.extend([n])
                    exits: bool = True
            else:
                return {'key': cls.session, 'is_true': True if StartClient(cls.session).checkAuth().get('status') == 'ok' else False, 'is_fake': exits, 'add': add, 'index_list': index}
            
        else:
            return {'key': cls.session, 'is_true': False, 'is_fake': True}
        
    def detecting(cls) -> (dict):
        return __Top(cls.session).__detecting()

class UpToDate(object):

    @classmethod
    def __init__(cls,
                 version: str, url: str) -> ...:
        cls._ver, cls._url = version, url
    
    def up(cls) -> (str):

        if str(get(cls._url).text) != cls._ver:
            return 'notUpdated'
        else:
            return 'isUpdated'
    
    def user(cls) -> (up):

        if cls.up() != 'isUpdated':
            if input('new version rubx now up to date? y/n : ').upper() == 'Y':
                system('pip install rubx --upgrade')
                if platform.system() == 'Windows':
                    system('cls')
                else:
                    system('clear')
        else:
            ... # is full version

class Clean(str):
    
    @staticmethod
    def html_cleaner(text: str) -> (str):
        return sub(compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), '', text)

class Scanner(object):
    
    @staticmethod
    def check_type(chat_id: str) -> (str):
             
            if len(chat_id) > 2:
                
                if   (chat_id.lower().startswith('g0')):
                    return ('Group')
                
                elif (chat_id.lower().startswith('c0')):
                    return ('Channel')
                
                elif (chat_id.lower().startswith('u0')):
                    return ('User')
                
                elif (chat_id.lower().startswith('s0')):
                    return ('Service')
                
                elif (chat_id.lower().startswith('b0')):
                    return ('Bot')
                else                            :
                    raise ValueError(f'CHAT ID \'{chat_id}\' NOT FOUND!')
            
            else:
                raise ValueError(f'CHAT ID \'{chat_id}\' FALSE!')

class Maker(object):

    @staticmethod
    def check_link(link: str, key: str) -> (str):
        
        from rb import StartClient
        
        with StartClient(key) as client:
            
            if link.startswith('@') or search(r'rubika\.ir/\w{4,25}', link):

                link: str = link.replace('https://', '').replace('rubika.ir/', '')
                result: dict = client.get_object_by_username(link.replace('@', '')).get('data')
                result: dict = result.get('user') or result.get('channel') or result.get('group')
                return result.get('user_guid') or result.get('channel_guid') or result.get('group_guid')
            
            elif len(link) == 56 or len(link) == 48 and 'joing' in link or 'joinc' in link:
                
                if 'joinc' in link:
                    return client.group_preview_by_join_link(link)['data']['group']['group_guid']
                elif 'joing' in link:
                    return client.channel_preview_by_join_link(link)['data']['channel']['channel_guid']

class Login(object):

    @staticmethod
    def SignIn(phone: str) -> (str):
        from rb import UserMethods
        return UserMethods.sign_in(phone, UserMethods.send_code(phone, input('send type is SMS/Interval : '), password=input('please enter your password : ') if input('insert password y/n : ').lower() == 'y' else None).get('data').get('phone_code_hash'), input('please enter activation code : ')).get('data').get('auth') or '0'

class Metas(object):
    
    def checker(text: str) -> (list):
        
        result, texts = [], text.replace('**', '', len(findall( r'\*\*(.*?)\*\*', text))).replace('__', '', len(findall(r'(\_\_(.*?)\_\_)', text))).replace('``', '', len(findall(r'\`\`(.*?)\`\`', text)))
        
        if ('**' in text):
            
            Bold: list = findall( r'\*\*(.*?)\*\*', text)
            boldFromIndex: list = [text.index(i) for i in Bold]
            [(result.append({'from_index': from_index, 'length': len(length), 'type': 'Bold'})) for from_index, length in zip(boldFromIndex, Bold)]
        
        if ('__' in text):
            
            Italic: list = findall(r'\_\_(.*?)\_\_', text)
            ItalicFromIndex: list = [text.index(i) for i in Italic]
            [(result.append({'from_index': from_index, 'from_index': len(length), 'type': 'Italic'})) for from_index, length in zip(ItalicFromIndex, Italic)]
        
        if ('``' in text):
            
            Mono: list = findall(r'\`\`(.*?)\`\`', text)
            monoFromIndex: list = [text.index(i) for i in Mono]
            [text.index(i) for i in Mono]
            [(result.append({'from_index': from_index, 'length': len(length), 'type': 'Mono'})) for from_index, length in zip(monoFromIndex, Mono)]
        
        return [result, texts]

class Tags(object):
    
    def checker(
        text : str,
        guids: list =   None,
        types: list =   None
        ) -> (list):
        
        if text.startswith('@') and text.endswith('@') and text.split().count('@') >= 2:
            
            (result, texts) = [], text.replace('@', '', len(findall(r'\@(.*?)\@', text)))
            
            Tags: list = findall(r'\@(.*?)\@', text)
            tagFromIndex: list = list(map(lambda i: text.index(i), Tags))
            
            [(result.append({'type': 'MentionText', 'mention_text_object_guid': guid, 'from_index': from_index, 'length': len(length), 'mention_text_object_type': mode})) for from_index, length, guid, mode in zip(tagFromIndex, Tags, guids, types)]
            
            return [result, texts]

class MetadataLoader(object):
    
    @classmethod
    def __init__(cls, caption: str,
                 metadata: dict = None) -> (None):
        cls.text, cls.meta = caption, metadata
    
    def making(cls) -> (dict):
        pass

class Device(dict):
    defaultDevice: dict = {
        'app_version'           :   'MA_2.9.8',
        'device_hash'           :   'CEF34215E3E610825DC1C4BF9864D47A',
        'device_model'          :   'rubx-lib',
        'is_multi_account'      :   False,
        'lang_code'             :   'fa',
        'system_version'        :   'SDK 22',
        'token'                 :   'cgpzI3mbTPKddhgKQV9lwS:APA91bE3ZrCdFosZAm5qUaG29xJhCjzw37wE4CdzAwZTawnHZM_hwZYbPPmBedllAHlm60v5N2ms-0OIqJuFd5dWRAqac2Ov-gBzyjMx5FEBJ_7nbBv5z6hl4_XiJ3wRMcVtxCVM9TA-',
        'token_type'            :   'Firebase'
    }

class Infos(str):
    citys, proxys, auth_, sent = [], [], [], lambda data: ('error' if data['status'].lower() != 'ok' else 'yeah')

class Filters:
    group, channel, user, chat, author = 'group_guid', 'channel_guid', 'user_guid', 'object_guid', 'author_object_guid'

class AccessList(object):
    
    class Admin(str):
        (
            PinMessages,
            setAdmin,
            ChangeInfo,
            BanMember,
            SetJoinLink,
            SetMemberAccess,
            DeleteGlobalAllMessages
            ) = (
                'PinMessages',
                'setAdmin',
                'ChangeInfo',
                'BanMember',
                'SetJoinLink',
                'SetMemberAccess',
                'DeleteGlobalAllMessages'
                )

    class User(str):
        (
            ViewMembers,
            ViewAdmins,
            SendMessages,
            AddMember
            ) = (
                'ViewMembers',
                'ViewAdmins',
                'SendMessages',
                'AddMember'
                )


class Encryption(object):
    
    @classmethod
    
    def __init__(cls, auth_key: str) -> ...:
        if len(str(auth_key)) != 32:
            raise IndexError('im so sorry for: len your session key is not \'32\'')
        cls.auth_key, cls.iv = bytearray((''.join(list(map(lambda a: chr((a - ord('a') + 9) % 26 + ord('a')), (str(auth_key[16:24] + auth_key[:8] + auth_key[24:32] + auth_key[8:16]).encode('latin-1')))))), 'utf-8'), bytearray.fromhex(str('0' * len(auth_key)))

    def encrypt(cls, data: str) -> (str):
        return (b64encode(new(cls.auth_key, MODE_CBC, iv=cls.iv).encrypt(pad(data.encode('utf-8'), block_size))).decode('utf-8'))

    def decrypt(cls, data: str) -> (str):
        return (unpad(new(cls.auth_key, MODE_CBC, iv=cls.iv).decrypt(urlsafe_b64decode(data.encode('utf-8'))), block_size)).decode('utf-8')

class MainError(Exception):
    pass

class NotREGISTERED(IOError):
    ...

class InvalidInput(IOError):
    ...

class TooREQUESTS(IOError):
    ...

class InvalidAUTH(IOError):
    ...

class ConnectError(OSError):
    pass

class ClientError(Exception):
    pass

class ServerError(
    Exception
    ):
    pass

class Errors:
    
    def MadeError(status: str, det: str) -> (bool or ...):

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

suffix: str = '.rbs'
rbs_version: int = 1

class SQLiteSession(object):

    def __init__(self, session: str) -> ...:
        self.filename = session
        if not session.endswith(suffix):
            self.filename += suffix

        self._connection = sqlite3.connect(self.filename,
                                           check_same_thread=False)
        cursor = self._connection.cursor()
        cursor.execute('select name from sqlite_master '
                       'where type=? and name=?', ('table', 'version'))
        if cursor.fetchone():
            cursor.execute('select version from version')
            version = cursor.fetchone()[0]
            if rbs_version != version:
                self.upgrade_database(version)

        else:
            cursor.execute(
                'create table version (version integer primary key)')
            cursor.execute('insert into version values (?)', (rbs_version,))
            cursor.execute('create table session (phone text primary key'
                           ', auth text, guid text, agent text)')
            self._connection.commit()
        cursor.close()

    def upgrade_database(self, version):
        pass

    def information(self) -> tuple:
        cursor = self._connection.cursor()
        cursor.execute('select * from session')
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(
        self        :   'SQLiteSession',
        phone_number:   str =   None,
        key         :   str =   None,
        guid        :   str =   None,
        url         :   str =   None
        ):
        cursor = self._connection.cursor()
        cursor.execute(
            'insert or replace into session (phone, auth, guid, agent)'
            ' values (?, ?, ?, ?)',
            (phone_number, key, guid, url)
        )
        self._connection.commit()
        cursor.close()

    @classmethod
    def from_string(cls, session: object,
                    file_name: str=None) -> (...):
        info = session.information()
        if file_name is None:
            if info is None:
                raise ValueError('file_name arg is not set')
            file_name = info[0]

        session = SQLiteSession(file_name)
        if info is not None:
            session.insert(*info)

        return session

class Urls(str):
    
    def get_url() -> (str):
        
        for i in range(3):
            try:
                return choice(list(loads(__import__('urllib').request.urlopen('https://getdcmess.iranlms.ir/').read().decode('utf-8')).get('data').get('API').values()))
            except Exception:
                continue

    giveUrl = lambda mode, key=None: SQLiteSession(key).information()[3] if key and 'https://' in SQLiteSession(key).information() else ('https://messengerg2c{}.iranlms.ir/'.format(str('56' if mode.lower() == 'mashhad' else '74' if mode.lower() == 'tehran' else str(randint(3, 74)))))

class clients(dict):
    (
        web,
        android,
        rubx
        ) = (
            {
                'app_name'      :   'Main',
                'app_version'   :   '4.1.11',
                'platform'      :   'Web',
                'package'       :   'web.rubika.ir',
                'lang_code'     :   'fa'
                },
            {
                'app_name'      :   'Main',
                'app_version'   :   '2.8.1',
                'platform'      :   'Android',
                'package'       :   'ir.resaneh1.iptv',
                'lang_code'     :   'fa'
                },
            {
                'app_name'      :   'Main',
                'app_version'   :   '3.0.8',
                'platform'      :   'Android',
                'package'       :   'app.rbmain.a',
                'lang_code'     :   'en'
                }
        )

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

            
            with session() as (
                sent
                ):

                for (i) in range(3):
                    
                    try:
                        
                        return (Make.evolution((sent).post(url, json=(data) if not mode else dumps(data), timeout=Connection.timeout, proxies=proxy).json(), (auth)))
                    
                    except Exception as e:
                        if i >= 2:
                            raise e
                else:
                    #finally:
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

class RubikaClient(object):

    def __init__(
        self                :   ('Client'),
        session_key         :   (str)                               =   (None),
        chat_id             :   (str)                               =   (None),
        username            :   (str)                               =   (None),
        app                 :   (str)                               =   ('rubx'),
        phone_number        :   (str)                               =   (None),
        device              :   (dict)                              =   (Device.defaultDevice),
        proxy               :   (dict)                              =   {'http': 'http://127.0.0.1:9050'},
        your_name           :   (str)                               =   (False),
        city                :   (str)                               =   ('mashhad'),
        banner              :   (bool)                              =   (False),
        creator_channel_open:   (bool)                              =   (False),
        platform            :   (str)                               =   (None),
        api_version         :   (typing.Union[str, int])            =   (None),
        headers             :   (typing.Union[dict, str, list])     =   (None),
        timeout             :   ((typing.Union[int, str]))          =   (5),
        check_update        :   (typing.Optional[bool])             =   (False),
        lang_code           :   (str)                               =   ('fa'),
        base_logger         :   (typing.Union[str, logging.Logger]) =   (None),
        check_session       :   (bool)                              =   (False),
        api_client          :   (str)                               =   (None)
        ) -> (None):
        
        '''
        # the main class
        ### inserts
        
        ## USE:
        
            `client = StartClient('session-key', 'u0...', 'username', 'rubx', your_name='saleh', banner=True, creator_channel_open=True, platform='rubx', api_version='5', timeout=5, proxy={'socks5':'http://127.0.0.1:9050'}, headers={'user-agent':...}, api_client='https://messengerg56c.iranlms.ir:80', ...)`

        ## EXAMPLES:
            
            `with StartClient(...) as client:`
                `client.send_message(...)`
            
            # ... or ...
            
            `client = StartClient()`
            `client.session_key = '' # len: 32 chars`
            
            `def run(callable, params) -> dict:`
                `return callable(**params)`

            ```
            print(
                run(
                    client.send_message,
                    dict(
                        chat_id='chat-guid',
                        text='Hey! this message from rubx lib.'
                        )
                    )
                )
            ```


        ## PARAMETERS:
        
            - 1- `self`: is a self obejct
            - 2- `session_key`: is account key [auth]
            - 3- `chat_id`: is your guid account
            - 4 - `username`: is your username account
            - 5 - `app`: is from app name
            - 6 - `phone_number`: is for using lib with phone_number and geting account key
            - 7 - `device`: is your account device for use token or thumbinline or ...
            - 8 - `your_name`: is for save info in a file.
            - 9 - `city`: is for your countery and city for using client server.
            - 10 - `banner`: is a boolean for print banner
            - 11 - `creator_channel_open`: is for joining your account in creator channel
            - 12 - `platform`: is for using user platform. examples: `rubx` or `web` or `android`
            - 13 - `api_version`: is for using api mode: `5` (for web and rubx) `4` (for rubika app [andorid]) `3` (for m.rubka.ir)
            - 14 - `headers`: is for set header to requests
            - 15 - `timeout`: is for requests timeout
            - 16 - `check_update`: is for checking lib new version
            - 17 - `lang_code`: to app lang code. `en`, `fa`, ...
            - 18 - `base_logger`: is for `__name__`
            - 19 - `check_session`: return a dict type to checking session [AUTH]
            - 20 - `api_client`: to set a server for requests
        
        
        ## `what is [guid]?` : guide unique identifier | chat id : group guid, channel guid and others ...
        ## `what is [session_key] or [auth]?`: is your session id (api key) for account.
        
        ### END
        '''
        
        (
            self.app,
            self.proxy,
            self.enc,
            self.city,
            self.platform,
            self.api_version,
            self.headers,
            self.username,
            self.chat_id,
            self.handling,
            self.phone,
            _log,
            self.timeout,
            self.lang_code,
            self.device,
            self.check_session,
            self.api_client
            ) = (
                app,
                proxy,
                Encryption(session_key),
                city,
                platform,
                api_version,
                headers,
                username,
                chat_id,
                {},
                phone_number,
                logging.getLogger(__name__),
                timeout,
                lang_code,
                device,
                check_session,
                api_client
                )
        
        Infos.citys.append(city)
        Infos.proxys.append(proxy)
        GetData.url: str = (api_client)

        if banner:
            assert list(map(lambda character: (print(character, flush=True, end=''), sleep(0.01)), f'\n\033[0m< \033[31mrubx \033[0m> \033[36m | \033[31mstarted in \033[0m{str(datetime.datetime.now())}\033[31m| \033[0m{Version.__version__}\n'))
        
        if your_name:
            open('session_info.sty', 'w+').write('name fan: '+your_name+'\ntime started: '+str(datetime.datetime.now())+f'\key: {session_key}'+'\nyour ip: '+str(get('https://api.ipify.org').text))
        
        if session_key:
            self.auth: (str) = (session_key)
            Infos.auth_.append(session_key)
        
        elif phone_number:
            Login.SignIn(phone_number)
            
        else:
            warn('SessionWarning: please insert session key or phone_number in object')
            
        if creator_channel_open:
            
            self.set_channel_action('c0BGS8Y01535a4510be64fafc4610d43', 'Join')
            webbrowser.open('https://rubika.ir/theClient')

        if (app == 'rubx'):

            try:
                open(f'{session_key}.sty', 'r')
            except FileNotFoundError:
                open(f'{session_key}.sty', 'w').write(session_key)
                database = SQLiteSession(session_key)
                database.insert(self.phone, session_key, self.chat_id, self.api_client or Urls.get_url())

        if check_update:
            UpToDate(Version.__version__, 'https://raw.githubusercontent.com/Mester-Root/rubx/main/rubx/__version__').user()
        
        if check_session:
            self.check_session: dict = __Top(self.session).detecting()
        
        if isinstance(base_logger, str):
            base_logger: str = logging.getLogger(base_logger)
        
        elif not isinstance(base_logger, logging.Logger):
            base_logger: str = base_log

        class Loggers(dict):
            def __missing__(self, key) -> ...:
                if key.startswith('rub.'):
                    key = key.split('.', maxsplit=1)[1]

                return base_logger.getChild(key)

        self._log = Loggers()
        
        Connection.timeout: int = timeout or 5
        clients.web.update({'lang_code': self.lang_code or 'en'}) # TODO: to set lang_code in rubx and android clients
        
    def __call__(self) -> (None):
        pass

    def __enter__(self):
        return (self)

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> (None):
        pass

    def start(self): # TODO: set runner with start func
        pass

    def get_auth(self) -> (str):
        return self.auth

Client = (RubikaClient)

class Method(Client):

    def from_json(
        self       : Client,
        method_name: str,
        **kwargs
        ) -> (
            dict
            ):

            data: dict = {}
            
            assert map(lambda key: data.update({key: kwargs.get(key)}, list(kwargs.keys())))

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   method_name[0].lower() + method_name[1:],
                    auth        =   self.auth,
                    data        =   data,
                    proxy       =   self.proxy,
                    platform    =   self.plaform or 'rubx',
                    mode        =   self.city
                )
            )

class UserMethods:


    def __enter__(
        self    :   (
            'Client'
            )
        ):
        return (
            self
            )

    def __exit__(
        self    :   (
            'Client'
            ),
        *args,
        **kwargs
        ) -> (...):
        ...

    # lambda func methods.

    # this method for logout and delete sessions
    log_out                     =   lambda self='Client': GetData.api(version='5', auth=self.auth, method='logout', mode=self.city, proxy=self.proxy, data={}, platform='web')

    # this methpd for getting all chats
    get_chats                   =   lambda self='Client', start_id=None: GetData.api(version=self.api_version or '5', auth=self.auth, method='getChats', data={'start_id': start_id}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)

    # this method for geting new chats
    get_chats_updates           =   lambda self='Client', state=None: GetData.api(version=self.api_version or '5', auth=self.auth, method='getChatsUpdates', data={'state'  :   state or str(round(datetime.today().timestamp()) - 200)}, mode=self.city, proxy=self.proxy, platform=self.platform or 'web')

    # it method is for get stickers 
    my_sticker_set              =   lambda self='Client': GetData.api(version=self.api_version or '5', method='getMyStickerSets', auth=self.auth, data={}, mode=self.city, proxy=self.proxy, platform=self.platform or 'web')

    # it method is for get account all folders
    get_folders                 =   lambda self='Client': GetData.api(version=self.api_version or '5', auth=self.auth, method='getFolders', data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)

    # setting methods

    get_privacy_setting         =   lambda self=Client: GetData.api(version=self.api_version or '5', method='getPrivacySetting', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_my_sessions             =   lambda self=Client: GetData.api(version=self.api_version or '5', method='getMySessions', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_two_passcode_status     =   lambda self=Client: GetData.api(version=self.api_version or '5', method='getTwoPasscodeStatus', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    check_two_step_passcode     =   lambda self, password: GetData.api(version=self.api_version or '5', method='checkTwoStepPasscode', auth=self.auth, data={'password': password}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    change_password             =   lambda self, password, new_password, new_hint: GetData.api(version=self.api_version or '5', method='changePassword', auth=self.auth, data={'password': password, 'new_password': new_password, 'new_hint': new_hint}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    turn_off_two_step           =   lambda self, password: GetData.api(version=self.api_version or '5', method='turnOffTwoStep', auth=self.auth, data={'password': password}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    setup_two_step_verification =   lambda self, password, hint: GetData.api(version=self.api_version or '5', method='setupTwoStepVerification', auth=self.auth, data={'password': password, 'hint': hint}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_block_users             =   lambda self: GetData.api(version=self.api_version or '5', method='getBlockUsers', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    request_recovery_email      =   lambda self, password, recovery_email: GetData.api(version=self.api_version or '5', method='requestRecoveryEmail', auth=self.auth, data={'password': password, 'recovery_email': recovery_email}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    verify_recovery_email       =   lambda self, password, code: GetData.api(version=self.api_version or '5', method='verifyRecoveryEmail', auth=self.auth, data={'password': password, 'code': code}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_contacts_updates        =   lambda self='Client', state=str(round(datetime.today().timestamp()) - 2000): GetData.api(version=self.api_version or '5', method='getContactsUpdates', auth=self.auth, data={'state': state}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_contacts                =   lambda self=Client : GetData.api(version=self.api_version or '5', method='getContacts', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_suggested_folders       =   lambda self=Client : GetData.api(version=self.api_version or '5', method='getSuggestedFolders', auth=self.auth, data={}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    get_chat_last_author        =   lambda self, chat_id: self.get_chat_info(chat_id).get('data').get('chat').get('last_message').get('author_object_guid')

    @staticmethod
    def key_generation() -> (str):
        
        '''
        this method for create a fake auth key
        '''
        
        key: (str) = ''.join(__import__('random').sample(str('qweertyuiopasdfghjklzxcvbnm' * 2), 32))
        
        return ''.join(list(map(lambda a: chr((a - ord('a') + ord('\t')) % ord('\x1a') + ord('a')), (str(key[16:24] + key[:8] + key[24:32] + key[8:16]).encode('latin-1')))))
            

    @staticmethod
    def tmp_generation() -> (str):
        
        '''
        this method for creating a tmp session
        '''
        
        tmp_session, strings = {}, sample('abcdefghijklmnopqrstuvwxyz', 32)
        list(map(lambda i: tmp_session.update({choice(strings): ''}), range(32)))
        
        return ''.join(list(tmp_session.keys()))

    @staticmethod
    def send_code(
        phone_number    :   (str),
        send_type       :   (str)   =   ('SMS'),
        password        :   (str)   =   None
        ) -> (
            dict
            ):

        '''
        send_type <- key/value -> SMS/Internal
        '''

        datas: dict = {'phone_number': f'98{phone_number[1:]}', 'send_type': send_type}
        if password:
            datas.update({'pass_key': password})
        return (GetData.api(version='5', tmp=UserMethods.tmp_generation(), method='sendCode', data=datas, mode=Infos.citys[0], platform='web'))

    @staticmethod
    def sign_in(
        phone_number    :   (str),
        phone_code_hash :   (str),
        phone_code      :   (str)
        ) -> (
            dict
            ):

        '''
        this method for login or signin with lib

        PARAMETERS:
            1- phone_number : phone number of target's account : 09XXXXXXXXX
            2- phone_code_hash : hash of code sent to phone
            3- phone_code : code sent to phone
        '''

        return GetData.api(
            version='5',
            method='signIn',
            mode=Infos.citys[0],
            platform='web',
            tmp=(UserMethods.tmp_generation()),
            proxy=Infos.proxys[0],
            data={
                'phone_number': f'98{phone_number[1:]}',
                'phone_code_hash': phone_code_hash,
                'phone_code': phone_code
                }
            )

    @staticmethod
    def register_device(auth: (str),
                        device: (dict) = Device.defaultDevice) -> (dict):
        
        '''
        this method for registering your acocunt
        '''
        
        return GetData.api(
            version='4',
            auth=auth,
            method='registerDevice',
            mode=Infos.citys[0],
            platform='android',
            proxy=Infos.proxys[0],
            data=(device)
            )

    @staticmethod
    def parsation (
        mode: (str),
        text: (str)
        ) -> (list):

        results: list = []

        if (mode.upper().startswith('HTML')):

            realText: (str)  = Clean.html_cleaner(text)
            bolds   : (list) = findall(r'<b>(.*?)</b>', text)
            italics : (list) = findall(r'<i>(.*?)</i>', text)
            monos   : (list) = findall(r'<pre>(.*?)</pre>', text)
            bResult : (list) = [realText.index(i) for i in bolds]
            iResult : (list) = [realText.index(i) for i in italics]
            mResult : (list) = [realText.index(i) for i in monos]

            [results.append({'from_index': bIndex, 'length': len(bWord), 'type': 'Bold'}) for bIndex, bWord in zip(bResult, bolds)]
            [results.append({'from_index': iIndex, 'length': len(iWord), 'type': 'Italic'}) for iIndex, iWord in zip(iResult, italics)]
            [results.append({'from_index': mIndex, 'length'        :   len(mWord), 'type'          :   'Mono'}) for mIndex, mWord in zip(mResult, monos)]

            return [results, realText]

        elif (mode.lower().startswith('markdown')):
            return (Metas.checker(text))
    
    def checkAuth(self) -> (dict):

        '''
        this method for checking your auth ke
        '''

        if (not 'NOT_REGISTERED' in list(
            (
                GetData.api(
                    version='4',
                    auth=self.auth,
                    method='',
                    data={},
                    mode=self.city,
                    proxy=self.proxy,
                    platform='android'
                )
                ).keys()
            )):
            
            return {
                'status'    :   'ok'
                }
        else:
            return {
                'status'    :   'error'
                }

    def request_send_file(
        self,
        file: (str)
        ) -> (dict):
        
        return GetData.api(
            version='5',
            method='requestSendFile',
            auth=self.auth,
            mode=self.city,
            platform='web',
            data={
                'file_name': str(file.split('/')[-1]),
                'mime': file.split('.')[-1],
                'size': Path(file).stat().st_size
                }
            )

    def upload_file(self, file: (str)) -> (dict):
        
        if (not 'http' in (file)):
            frequest, bytef = UserMethods.request_send_file(self, file), open(file, 'rb+').read()
            hash_send: str = frequest['access_hash_send']
            file_id: str = frequest['id']
            url: str = frequest['upload_url']
            
            header: dict = {
                'auth'              :   self.auth,
                'Host'              :   url.replace('https://', '').replace('/UploadFile.ashx', ''),
                'chunk-size'        :   str(Path(file).stat().st_size), 
                'file-id'           :   str(file_id),
                'access-hash-send'  :   hash_send,
                'content-type'      :   'application/octet-stream',
                'content-length'    :   str(Path(file).stat().st_size),
                'accept-encoding'   :   'gzip',
                'user-agent'        :   'okhttp/3.12.1'
            }
            
            if len(bytef) <= 131072:
                
                header['part-number'], header['total-part'] = '1', '1'
                
                while (1):
                    
                    try :
                        j = post(data=bytef, url=url, headers=header).text
                        j: (dict) = loads(j)['data']['access_hash_rec']
                        break
                    except Exception:
                        continue
        
                return [frequest, j]
            
            else:
                t: (int) = round(len(bytef) / 131072 + 1)
                
                for i in range(1,t+1) :
                    if i != t :
                        k = i - 1
                        k = k * 131072
                        while 1:
                            try:
                                header['chunk-size'], header['part-number'], header['total-part'] = '131072', str(i), str(t)
                                o = post(data=bytef[k:k + 131072], url=url, headers=header).text
                                o = loads(o)['data']
                                break
                            except Exception:
                                continue
                    else:
                        k = i - 1
                        k = k * 131072
                        while (1):
                            try:
                                header['chunk-size'], header['part-number'], header['total-part'] = str(len(bytef[k:])), str(i), str(t)
                                p = post(data=bytef[k:], url=url, headers=header).text
                                p = loads(p)['data']['access_hash_rec']
                                break
                            except Exception:
                                continue
                        return [frequest, p]

        else:
        
            frequest: (dict) = GetData.api(
                method='requestSendFile',
                auth=self.auth,
                mode=self.city,
                proxy=self.proxy,
                platform='web',
                data={
                    'file_name' :   file.split('/')[-1],
                    'mime'      :   file.split('.')[-1],
                    'size'      :   len(get(file).content)
                    }
                )
            
            hash_send: (str) = frequest['access_hash_send']
            file_id: (str) = frequest['id']
            url: (str) = frequest['upload_url']
            bytef: (str) = get(file).content
            
            header: (dict) = {
                'auth'              :   self.auth,
                'Host'              :   url.replace('https://', '').replace('/UploadFile.ashx', ''),
                'chunk-size'        :   str(len(get(file).content)),
                'file-id'           :   str(file_id),
                'access-hash-send'  :   hash_send,
                'content-type'      :   'application/octet-stream',
                'content-length'    :   str(len(get(file).content)),
                'accept-encoding'   :   'gzip',
                'user-agent'        :   'okhttp/3.12.1'
            }
            
            if len(bytef) <= 131072:
                header['part-number'], header['total-part'] = '1', '1'
                while (1):
                    try:
                        j = post(data=bytef, url=url, headers=header).text
                        j = loads(j)['data']['access_hash_rec']
                        break
                    except Exception:
                        continue
                return [frequest, j]
            
            else:
                t: (int) = round(len(bytef) / 131072 + 1)
                for i in range(1,t+1):
                    if (i != t):
                        k = i - 1
                        k = k * 131072
                        while 1:
                            try :
                                header['chunk-size'], header['part-number'], header['total-part'] = '131072', str(i), str(t)
                                o = post(data=bytef[k:k + 131072], url=url, headers=header).text
                                o = loads(o)['data']
                                break
                            except Exception:
                                continue
                    else:
                        k = i - 1
                        k = k * 131072
                        
                        while (1):
                            try:
                                header['chunk-size'], header['part-number'], header['total-part'] = str(len(bytef[k:])), str(i), str(t)
                                p = post(data=bytef[k:], url=url,headers=header).text
                                p = loads(p)['data']['access_hash_rec']
                                break
                            except Exception:
                                continue
                        return [frequest, p]

    @staticmethod
    def get_thumb_inline(
        image_bytes: (bytes)
        ) -> (bytes):
        
        from base64 import b64encode
        from io import BytesIO

        from PIL.Image import ANTIALIAS
        from PIL.Image import open as openF
        
        im: (bytes) = openF(BytesIO(image_bytes))
        (width, height) = (im.size)
        
        if (height > width):
            new_height: (int) = (40)
            new_width: (int)  = round(new_height * width / height)
        else:
            new_width: ((int))  = 40
            new_height: (int) = round(new_width * height / width)
        im = im.resize((new_width, new_height), ANTIALIAS)
        changed_image: (bytes) = BytesIO()
        im.save(changed_image, format='PNG')
        changed_image: (bytes) = changed_image.getvalue()

        return (b64encode(changed_image))
    
    @staticmethod
    def get_image_size(
        image_bytes: (
            bytes
            )
        ) -> (list):
        
        from io import BytesIO

        from PIL.Image import open as openF
        
        im = openF(BytesIO(image_bytes))
        (width, height) = (im.size)
        
        return [
            width,
            height
            ]

    def send_message(
        self                :   ('Client'),
        text                :   (str)   =   None,
        chat_id             :   (str)   =   None,
        username            :   (str)   =   None,
        link                :   (str)   =   None,
        metadata            :   (list)  =   None,
        button_id           :   (str)   =   None,
        sticker             :   (bool)  =   (False),
        emoji_character     :   (str)   =   ('😜'),
        sticker_id          :   (str)   =   ('5e07caefc34bb4876ca8a625'),
        sticker_set_id      :   (str)   =   ('5e07cac2c34bb4876ca8a624'),
        file_id             :   (str)   =   ('499582666'),
        w_h_ratio           :   (str)   =   ('1.0'),
        reply_to_message_id :   (str)   =   None,
        parse_mode          :   (str)   =   None
        ) -> (typing.Union[dict, None,]):

            '''
            # this method for sending a message
            
            ## USE:
                - `self.send_message('**hey** __from__ ``rubx``', 'u0...')`
            '''

            if (username or link):
                chat_id: str = Maker.check_link(link=username or link, key=self.auth)

            data: (dict) = {
                    'object_guid'           :   (chat_id),
                    'rnd'                   :   str(randint(100000,999999999)),
                    'text'                  :   (text),
                    'reply_to_message_id'   :   (reply_to_message_id)
                }

            if sticker:
                data.update(
                    {
                        'sticker': {
                            'emoji_character'       :   emoji_character,
                            'w_h_ratio'             :   w_h_ratio,
                            'sticker_id'            :   sticker_id,
                            'file'                  :   {
                                'file_id'           :   file_id,
                                'mime'              :   'png',
                                'dc_id'             :   '32',
                                'access_hash_rec'   :   '911095004325419223254883204658',
                                'file_name'         :   'sticker.png'
                                },
                            'sticker_set_id'        :   sticker_set_id
                            }
                        }
                    )

            if button_id:
                data['aux_data']: (dict) = {'button_id' : button_id}
            
            if metadata and isinstance(metadata, list):
                data['metadata']: (dict) = {'meta_data_parts' : metadata}
            
            if (parse_mode or text.startswith('__') or text.startwith('**') or text.startswith('``')):
                base: list = UserMethods.parsation(str('HTML' if len(findall(r'(<.*?>)', text)) >= 2 else 'markdown'), text)
                data.update({'metadata': {'meta_data_parts':   base[0]}, 'text': base[1]})
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy,
                    data        =   data
                    )
                )

    def edit_message(
        self        :   ('Client'),
        message_id  :   (str),
        new_text     :   (str),
        chat_id     :   (str)   =   (None),
        username    :   (str)   =   (None),
        link        :   (str)   =   (None),
        metadata    :   (list)  =   (None)
        ) -> (dict or ...):
        
        '''
        this method for edit message
        
        self.edit_message('300000000', '<b> edited </b>', 'u0...')
        '''
        
        if (username or link):
            chat_id: str = Maker.check_link(link=username or link, key=self.auth)

        data: (dict) = {
            'message_id'    :   message_id,
            'object_guid'   :   chat_id,
            'text'          :   new_text
        }

        if metadata and isinstance(metadata, list):
            data.update({'metadata': {'meta_data_parts' : metadata}})

        if (new_text.startswith('__') and new_text.endswith('__') or
            new_text.startswith('**') and new_text.endswith('**') or
            new_text.startswith('``') and new_text.endswith('``') or
            search(r'<.*?>', new_text)):

            base: list = UserMethods.parsation('HTML' if len(findall(r'(<.*?>)', new_text)) >= 2 else 'markdown', new_text)
            data.update({'metadata': {'meta_data_parts':   base[0]}, 'text': base[1]})

        return (
            GetData.api(
                version     =   self.api_version or '5',
                auth        =   self.auth,
                method      =   'editMessage',
                data        =   data,
                platform    =   self.platform or 'web',
                proxy       =   self.proxy,
                mode        =   self.city
            )
        )

    def get_stickers_by_set_ids(
        self            :   ('Client'),
        sticker_set_ids : (
            list
            )
        ) -> (dict or ...):

        '''
        sticker ids:  ['5e0c957a6282726921b7634n', '6e0c957a6282726921b7635l']
        '''
        
        return (
            GetData.api(
                version     =   self.api_version or '5',
                auth        =   self.auth,
                method      =   'getStickersBySetIDs',
                mode        =   self.city,
                proxy       =   self.proxy,
                platform    =   self.platform or 'web',
                data        =   {
                    'sticker_set_ids'   :   sticker_set_ids
                    },
            )
        )

    def delete_messages(
        self        :   ('Client'),
        message_ids :   (list),
        chat_id     :   (str)   =   (None),
        username    :   (str)   =   (None),
        link        :   (str)   =   (None),
        the_type    :   (str)   =   ('Global')
        ) -> (
            dict
            ):
        
        '''
        # THIS METHOD FOR DEL MESSAGES SELECTED.
        
        ## EXAMPLE:
            - `self.deleteMessages(['1234566', ], 'TARGET-GUID')`
        
        ## PARAMETRS:
            - its a `self` object
            - `message_ids` is for all message ids in list
            - `chat_id` is chat or target guid
            - `username` for dont using of chat_id parameter and to insert this parameter: '@username'
            - `link` for dont using chat_id or username parameters and to insert: 'https://rubika.ir/username'
        '''
        
        if (username or link):
            chat_id: str = Maker.check_link(link=username or link, key=self.auth)
  
        return (GetData.api(
            version =   self.api_version or '5',
            method  =   'deleteMessages',
            auth    =   self.auth,
            data    =   {
                'object_guid'   :   chat_id,
                'message_ids'   :   message_ids,
                'type'          :   the_type
                    },
            platform=   self.platform or 'web',
            mode    =   self.city,
            proxy   =   self.proxy
        ))

    def get_messages_interval(
        self                :   (Client),
        middle_message_id   :   (str)   =   '0',
        sort                :   (str)   =   'FromMin',
        chat_id             :   (str)   =   (None),
        username            :   (str)   =   (None),
        link                :   (str)   =   (None),
        ) -> (
            dict
            ):

        '''
        # THIS METHOD FOR GET MESSAGES A CHAT (MIN)
        
        ## EXAMPLE:
            `self.get_messages_interval(min_id='last_message_id', sort='FromMin', chat_id='target-guid')`
        
        ## PARAMETERS:
            - `middle_message_id` or middle message id is chat last message id
            - `sort` is the time messages
            - `chat_id` is target guid or uid chat
            - `username` for do not using chat_id! to insert: '@username'
            - `link` for dont using username or chat__id! to insert: 'https://rubika..ir/username'
        '''
        
        if (username or link):
            chat_id: str = Maker.check_link(link=username or link, key=self.auth)
        
        return (
            GetData.api(
                version     =   self.api_version or '5',
                auth        =   self.auth,
                method      =   'getMessagesInterval',
                data        =   {
                    'object_guid'       :   chat_id,
                    'sort'              :   sort,
                    'middle_message_id' :   middle_message_id
                    },
                mode        =   self.city,
                platform    =   self.platform or 'web',
                proxy       =   self.proxy,
                )
            )

    def get_object_by_username(
        self        :   (Client),
        username    :   (str)
        ) -> (
            dict
            ):

        '''
        username is @theUsername
        '''

        return (GetData.api(
            version =   '5',
            auth    =   self.auth,
            method  =   'getObjectByUsername',
            data    =   {
                'username'  :   username.replace(
                    '@',
                    ''
                    )
                },
            platform=   'web',
            mode    =   self.auth,
            proxy   =   self.proxy,
            
        ))

    def get_messages_by_id(
        self        :   ('Client'),
        chat_id     :   (str),
        message_ids :   (list)
        ) -> (
            dict
            ):
            
            '''
            self.get_messages_by_id('chat guid', ['12345...', ...])
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is target guid
                3- message_ids is all message id in list class
            '''
            
            return (
                GetData.api(
                    version =   '5',
                    method  =   'getMessagesByID',
                    auth    =   self.auth,
                    data    =   {
                        'object_guid'   :   (
                            chat_id
                            ),
                        'message_ids'   :   (
                            message_ids
                            )
                        },
                    mode    =   self.city,
                    proxy   =   self.proxy,
                    platform=   'web'
                    )
                )

    def forward_messages(
        self                :   ('Client'),
        from_object_guid    :   (str),
        message_ids         :   (list),
        to_object_guid      :   (str)
        ) -> (dict):

            '''
            # THIS METHOD FOR FORWARD MESSAGE.
            
            ## USE:
                `self.forward_messages('from chat guid', ['1234...', ], 'to chat guid')`
            
            ## PARAMETERS:
                - `self` is a self object
                - `from_object_guid` is for forwarded from a chat guid
                - `message_ids` its a list for message ids
                - `to_object_guid` is for forwarding to a chat_guid
            
            ### END
            '''

            return(
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'forwardMessages',
                    auth        =   self.auth,
                    data        =   {
                        'from_object_guid'  :   from_object_guid,
                        'message_ids'       :   message_ids,
                        'rnd'               :   str(randint(100000,999999999)),
                        'to_object_guid'    :   to_object_guid
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def seen_chats(
        self        :   ('Client'),
        seen_list   :   (dict)
        ) -> (
            (
            dict
            ) or (
                ...
                )
            ):

        '''
        USE:
            self.seenChats({'guid':'message_id'})
        PARAMMETERS:
            1- self is a self object
            2- seen_list is a dictionary or list for seening all messages
        END.
        '''
        
        return(
            GetData.api(
                version     =   '5',
                method      =   'seenChats',
                auth        =   self.auth,
                data        =   {
                    'seen_list'  :   seen_list
                    },
                mode        =   self.city,
                proxy       =   self.proxy,
                platform    =   self.platform if self.platform else 'web'
            )
        )

    def send_chat_activity(
        self        :   ('Client'),
        activity    :   (str),
        chat_id     :   (str)   =   (None),
        username    :   (str)   =   (None),
        link        :   (str)   =   (None),
        ) -> (dict) or (...):

            '''
            this method for send typeing... in chat
            
            USE:
                self.send_chat_activity('typing...', 'user guid')
            PARAMETERS:
                1- self is a self object
                2- activity is for send a text in chat
                3- chat_id is chat guid
                4- username for dont using chat_id
                5- link for dont using chat_id or username.
            END
            
            '''

            if (username or link):
                chat_id: str = Maker.check_link(link=username or link, key=self.auth)            
            
            return(
                GetData.api(
                    version     =   '5',
                    method      =   'sendChatActivity',
                    auth        =   self.auth,
                    data        =   {
                        'activity'      :   activity,
                        'object_guid'   :   chat_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   'web'
                )
            )

    def set_pin_message(
        self        :   ('Client'),
        chat_id     :   (str),
        message_id  :   (str),
        action      :   (str)   =   ('Pin')
        ) -> (
            dict
            ) or (
                ...
                ):

            '''
            USE:
                self.set_pin_message('chat guid', 'message id')
            PARAMETERS:
                1- self is a self object
                2- chat_id is chat guid
                3- message_id is chat (others) message id
                4- action is actions type: 'Pin' and 'Unpin'
            END
            '''
            
            return (
                GetData.api(
                    version='4',
                    method='setPinMessage',
                    auth=self.auth,
                    data= {
                        'action'        :   action,
                        'message_id'    :   message_id,
                        'object_guid'   :   chat_id
                        },
                    mode=self.city,
                    proxy=self.proxy,
                    platform= self.platform or 'android'
                )
            )

    def set_block_user(
        self        :   ('Client'),
        chat_id     :   (str),
        action      :   (str)   =   ('Block')
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            ## USE:
                `self.set_block_user('user guid', action='Block')`
            ## PARAMETERS:
                - self is a self object
                - chat_id is user guid
                - action is actions type: 'Block' and 'Unblock'
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'setBlockUser',
                    auth        =   self.auth,
                    data        ={
                        'action'    :   action,
                        'user_guid' :   chat_id
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web',
                    headers     =   self.headers
                )
            )

    def send_photo(
        self                :   ('Client'),
        chat_id             :   (str),
        file                :   (str),
        size                :   (list)  =   [],
        thumbnail           :   (str)   =   ('iVBORw0KGgoAAAANSUhEUgAAABwAAAAoCAYAAADt5povAAAAAXNSR0IArs4c6QAACmpJREFUWEfNVwl0U1Ua/u57ycuetGmatOneJt0prWUpYEVBkB0dQFkcGQRRYZwB5AyLy3gAHSgqjqgjokg944oiCiguI6ioFbpQSimFlkK3hO5p0uzv3TkJTaciwsyZOZ6557yTd/Lu/b97/+X7v0vwKw/yK+Ph/xowsLnBT8g5AgDa/1zXYdc7YQggYChg+FqD6f94TfBrAYYMBICY+CHQxMch1WBAMsSItHhBHS60e7pQZ7Wi3laF7n7A0CavusGrAQ4syJloUAzPtRVk3uBdlGgWbtGoEe0lhJzpJWjsoyCEAjz87l5YeprwVWMpir/bha/73Ruw87PTXgkYBJsDkNwnkrKSRrhWac3dcyjvlfs9QKcLtLaH+m0eCCwDuCEibqJkfIxcRMUS8IKiu6sj+kBtif6llu1vlvTHPHDwAHBwDAYMgi3NV2nnptH5eaOFVfXDnAnnJRA4P/ztHrC1Lpa1IBItJBdNfBY6fFFw+pXUB4kfrIRCJmWIXiViFeJmtqL6ec+KzS+gudk9KLYDgAEw5pmbYBytx+qCFDzUlQpUZoLvlhLSzrPsjw69UNmR333OktFgd6ic4MQM4rUGkmyMITqNXBCDgvoovELgIYRle0lL29+FxY89gro6ewh0IM2fGA79bUl4aGQM1nnDCG3PA62Mp0yrn3F9eVx2/JtDxmJrGVOGTns3XK1NQQMmk0QplSZHJedOjkkZ+luanjj0fIqUt8RJBF7GssRPeklj2+vCsg3rcPq0P+Da4MkmGiArmoA7h4TjBV4EqS+V0LpsypSKcGHvO3j64B7sRiucMA6PA8+bcan8cH84BpIiT55nNEVmLkuIzf69PS1MWTFS7aseGcH0acVWlFRuxZ2rXgxgBU94bgFGqiXkpQglzaVK8H15YEq1qC4qxprP38Cn/e7gxIaZeUSpm8aLXRX8mbc+vKIMqE6nU+Sop842q5KKYjmZtsso9laO1QvnM1QnOoqeW+o4fLiaLDUadQvT2QdGJbg28MoOgYknxJJAzz7yBf5cvBPvA2BVKqPmxtvmLJw6Y/baEQXDdA2W5q4P93/27jsvPLkFbsvFwQyk1ZoUqZHjFiRpkp5JZgin8VO4ROhpE2yvvnhs83pSkTp2eHi4d3tswqVhQlyD4IqB/bSP7hy1BusDYMCI2El3zluz5L7bl44x29HTx/McQ5kezkg3f9773Z6181bCVlYxKONJetTNcRpV6toEbfrSBJGHalgR8fL+kv11ex8jlVk33ZOp4XbQyIsSJuMctUWTktm76NLDlagJAkrGxWeNmvRo/vS5C10RBqGqRcTGaCk1GQThZEPniR82zVuB7iPfBeKDAA1c/iUPZC8pdDOq112S6ASzROBZUGuTrelrcjRrzLYCteqPft1FwZd6pu+CnO4eshErBiWFFJEb5yK2cCfyC1koCIVHALzdvbCU7Man01f3F3aIxIOJuDHOlKhUmB7tVd6wsIYJEzIlgt8nCN3k1NDC/ely1WSfxiL0mqob32r1blq5F8X9O73Mh0pDJGdYeD8S71jPJ+VwqkgOUVxrl6V0317X969t93afPHUFkZD88HDV03FJi/TylKLt3gwfOIU8SQxKmnPHVhgkihyfsktwxNdU/anKtmp3aZAPA64JABKoJpmhLXwcKXPuQnoyYRQMI2MFKvG4qNR50WLmviwu3/3YNrvd3jnIM6LKQtPMeFHEayfs6eLXiYkoRTIpaRg2/lQ8y2X4xU449BeOLa66+OC+c6gctBDQry5gwsw75Lnjs0VmHbU51Yxe6qOpkk7UtzBEkUQ702yHdh7YsuiRQTRGTszUTojyad+Qd6VqD/sNfftpHMi6YQ+Xz+DsWfm0Hr2KnoolDWXL99WjfBAgo4yank5U+U+p0sdNl2cbhDq3mZWIKI2gF7uEH49YOyNuyVAMlZV6d81Y7mw6VtbvHXryXtwW7da/EdGYrfP7ON4J4iVTctaW5Ck1+TNR600Qztc9bq1Zs+NC++f9gMFemHdv8USX2/Dq+eaoaK85FdBKAIEKcF+qx6F1r4IkhkNfMB3tHz2LczsC8ScmE0TvTcRvMhnNLrY6Uyo4tJRhfYSMz/zDnhhl/B154j6+kD9rrb1UtnVBw5kgDV2OYaxUfNebc8AlvULrLRI+KoYiKRoEVAB/qZ4c2bqBP/Hch4BUD4gdQDCOzM35CH90BO67RaN40ldqBrHFgLC8QG5MW7bJoEpar2N5ZIqdzhTX6bemlb2/HECAbAODw5SjsyDSF6OpUUQ0OtCMbAqOoXBaK3Bw/gq0Hvl+kAQJlsXfFiNjiI48NUrMTfWVJQukPdntoW4LmZCx8g6pJOI1jmXCYiUiIZJ4Th6q/2DVUeuJf2Vq5O+GgjrmQVD1MQmz7gu/cWyMMVFCu9s6jze/PHU5bOUBpgkVPjEB4veKMM2kILvkDSKlUJdAXc2mC9/2WvaRkUn35Khk+i1qqWEiQ7xCDMd6xbxjz9PHNj2IQFO/PIIdWz/77dF5QxJemTIpP7Ozo8/n77tUVrRy8cP+lu8Hd3dmw0pkjDBiywQNmcSfYASmw0hcDRlfza8pXUF0ujRVRtTku7WymO2Mxw0pyyKMo229zvrn36zatTlEVQFQpSFFN+butUuih83Y0OnVMFG89dDOe4cuAGw9l3kXdNw0RM25FStnpWGVthwCbSFwuxXWqpMxfx1dWrs16G/lxNWZjDziL1qJYWpsaztvcPBMGPW3tjtqtn1c9/bz/RwZMIi8yfenRg4t2GDIGjbSWvLZzi9eXF0EwBeYkzMZsZOmYcX04ViRexZEfgrgbRA8DP4x5QAWfXsR1lDHF2HBtluhitghgig2vMfOx3a5GaPd2+vurP+o+sKXW63euuqQENJqtWqn0xnudrsDrQlIhDRvlGhkwXh+zbjhdHJaB2h6FSjOg/b5Sc07FXTdgz/g4EADDi6KzFSg8O67SFTKsxSCCpTnxX6B0booI+3tbrNfOn3A1l75Cd/edArE0Q51HKDWxMuzo28wj+iYPmbI6fGjozqVei+laY2UxlYCrjbSVN5Ki276GC+H6jqk2i6fNDlfhSFT55LotE2UMhHw+QRwIkApY6FWAWEyIFzkh4Z1ctJeJoY7Jc9gDzJZOIosro+Gi8Gr+0Dya8DSalw4VoeiCQcHwIJy5GcyEYmJnCR91ljGnPk4MUeOhpEIjBw+MeeiMrGdUaOFNfhPs0a+FGH+ehrJUr9JDaoWExZiyho9jDfuW/bH99+lTz50zB9irAHtczUhHCyDnAdG62OyHfOj09uXySQ2M/F6QLw8GH+QfihlgGgFIWlhBCqZAMoQoc8uOl9bzu34oIjZXXb2J53jqkI4lBM/Ech5MxAdZsbthgxMURtIDisjBk5MuCQZhUlOPX0OamltRGXtSXxa9g0+Of4NAhLyF+8X17rMXLmIRGZCIZXBwBCoFYFa8MDWY0VbezscVyq4X7q+Xe+6FrAT1CiDZMRgT4TeQ3NCMuNqc4L//TuAV7p6cGaHkmEgRr+IdIUGud68/9n3//SE/zXwrw74T3XSTDJjBhdXAAAAAElFTkSuQmCC'),
        caption             :   (str)   =   (None), 
        reply_to_message_id :   (str)   =   (None),
        parse_mode          :   (str)   =   (None)
        ) -> (dict or...):
            
            
            '''
            # this method for send photo image
            
            ## USE:
                `self.send_photo('chat-guid', 'path/*.jpg')`
                
            ## PARAMETERS:
                - `self` is a self object
                - `chat_id` is chat guid (other)
                - `file` is file path
                - `size` is file size = none
                - `thumbnail` is file thumbnail
                - `caption` is message file caption
                - `reply_to_message_id` is for reply to message id in object
                - `parse_mode`: to use the metadata params = 'markdown', 'html'
            '''
            
            uresponse: (dict) = UserMethods.upload_file(self, file)
            
            if ('.' in thumbnail):
                thumbnail: str = str(UserMethods.get_thumb_inline(open(file, 'rb').read() if not 'http' in file else get(file).content))
            if (size == []):
                size: list = UserMethods.get_image_size(open(file, 'rb').read() if not 'http' in file else get(file).content)
            
            file_inline: (dict) = {
                'dc_id'             :   uresponse[0]['dc_id'],
                'file_id'           :   uresponse[0]['id'],
                'type'              :   'Image',
                'file_name'         :   file.split('/')[-1],
                'size'              :   str(len(get(file).content if 'http' in file else open(file, 'rb').read())),
                'mime'              :   file.split('.')[-1],
                'access_hash_rec'   :   uresponse[1],
                'width'             :   size[0],
                'height'            :   size[1],
                'thumb_inline'      :   thumbnail
            }
            
            data: (dict) = {
                        'file_inline'           :   file_inline,
                        'object_guid'           :   chat_id,
                        'rnd'                   :   str(randint(100000,999999999)),
                        'reply_to_message_id'   :   reply_to_message_id
                    }
            
            if (parse_mode):
                base: list = UserMethods.parsation(str('HTML' if len(findall(r'(<.*?>)', text)) >= 2 else 'markdown'), text)
                data.update({'metadata': {'meta_data_parts':   base[0]}, 'text': base[1]})
                data.update({'text': base[1]})
                caption: bool = False
            
            if (caption):
                data.update({'text': caption})
            
            return (
                GetData.api(
                    version     =   '5',
                    method      =   'sendMessage',
                    auth        =   self.auth,
                    data        =   data,
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def send_voice(
        self                :   ('Client'),
        file                :   (str),
        time                :   (str),
        chat_id             :   (str)   =   (None),
        caption             :   (str)   =   (None),
        reply_to_message_id :   (str)   =   (None),
        ) -> (dict or ...):
            
            '''
            # this method for send voice
            
            ## USE:
                `self.send_vvoice('path/file.mp3', '999')`
            
            ## PARAMETERS:

                - `self` is a self object
                - `file` is file path (music)
                - `time` is voice time
                - `chat_id` is chat guid
                - `caption` is message caption
                - `reply_to_message_id` is for reply to a message
            '''
    
            uresponse: (list) = UserMethods.upload_file(self, file)
            
            the_data: (dict) = {
                        'file_inline'           :   {
                            'dc_id'             :   uresponse[0]['dc_id'],
                            'file_id'           :   uresponse[0]['id'],
                            'type'              :   'Voice',
                            'file_name'         :   file.split('/')[-1],
                            'size'              :   str(len(get(file).content if 'http' in file else open(file, 'rb').read())),
                            'time'              :   time,
                            'mime'              :   file.split('.')[-1],
                            'access_hash_rec'   :   uresponse[1],
                        },
                        'object_guid'           :   chat_id,
                        'rnd'                   :   str(randint(100000,999999999)),
                        'reply_to_message_id'   :   reply_to_message_id
                        }
            
            if caption:
                the_data['text']: (str) = caption
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'sendMessage',
                    auth        =   self.auth,
                    data        =   the_data,
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                    )
            )

    def send_document(
        self                :   ('Client'),
        file                :   (str),
        chat_id             :   (str)   =   (None),
        caption             :   (str)   =   (None),
        reply_to_message_id :   (str)   =   (None),
        ) -> (
            dict
            or
            ...
              ):
            
            '''
            this method for send all files *
            
            
            USE:
            
                self.send_document('chat-guid', 'path/file.*')
            PARAMETERS:
            
                1- self is a self object
                
                2- chat_id is chat guid (other)
                
                3- file is file path
                
                4- caption is message file caption
                
                5- reply_to_message_id is for reply to message id in object
            '''
            
            uresponse: list[str, ] = UserMethods.upload_file(self, file)
            
            data: (dict) = {
                    'object_guid'           :  chat_id,
                    'reply_to_message_id'   :   reply_to_message_id,
                    'rnd'                   :   str(randint(100000,999999999)),
                    'file_inline'           :   {
                        'dc_id'             :   str(uresponse[0]['dc_id']),
                        'file_id'           :   (str(uresponse[0]['id'])),
                        'type'              :   'File',
                        'file_name'         :   file.split('/')[-1],
                        'size'              :   str(len(get(file).content if 'http' in file else open(file, 'rb').read())),
                        'mime'              :   file.split('.')[-1],
                        'access_hash_rec'   :   uresponse[1]
                    }
                }
            
            if caption:
                data['text']: (str) = caption
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'sendMessage',
                    auth        =   self.auth,
                    data        =   data,
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def send_location(
        self                :   ('Client'),
        chat_id             :   (str),
        location            :   list[str, ],
        reply_to_message_id :   (str)   =   (None),
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            this method for send your location
            
            USE:
                self.send_location('chat-guid', 'loc')
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is chat guid (other)
                3- location is your loc
                4- reply_to_message is for reply message
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    methood     =   'sendMessage',
                    auth        =   self.auth,
                    data        =   {
                        'is_mute'               :   False,
                        'object_guid'           :   chat_id,
                        'rnd'                   :   str(randint(100000,999999999)),
                        'location'              :   {
                            'latitude'          :   location[0],
                            'longitude'         :   location[1]
                            },
                        'reply_to_message_id'   :   reply_to_message_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def upload_avatar(
        self        :   ('Client'),
        file        :   (str),
        chat_id     :   (str)   =   (None),
        thumbnail   :   (str)   =   (None),
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            this for upload avatar (profile image)
            
            USE:
                self.upload_avatar('file', 'your-guid')
            
            PARAMEETERS:
                1- self is a self object
                2- main is file
                3- chat_id is your chat id
                4- thumbnail is for thumbnail photo
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'uploadAvatar',
                    auth        =   self.auth,
                    data        =   {
                        'object_guid'       :   self.chat_id or chat_id,
                        'thumbnail_file_id' :   str(UserMethods.upload_file(self, thumbnail or file)[0]['id']),
                        'main_file_id'      :   str(UserMethods.upload_file(self, file)[0]['id'])
                        },
                    modee       =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web',
                    headers     =   self.headers or {
                        'accept'        :   'application/json',
                        'user-agent'    :   __import__('pyuseragents').random()
                        }
                )
            )

    def get_chat_info(
        self    :   (Client),
        chat_id :   (str)
        ) -> (dict):

            '''
            # THIS METHOD FOR GETTING ALL CHAT INFO!
            
            ## EXAMPLE:
                - `self.get_chat_info('chat-guid') # all object`
            ## PARAMS:
                - `chat_id` is obj guid
            ### END
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   f'get{str(Scanner.check_type(chat_id))}Info',
                    auth        =   self.auth,
                    data        =   {
                        f'{Scanner.check_type(chat_id).lower()}_guid' :   chat_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def send_gif(
        self                :   Client,
        chat_id             :   str,
        file                :   str,
        width               :   str,
        height              :   str,
        thumbnail           :   str =   'iVBORw0KGgoAAAANSUhEUgAAABwAAAAoCAYAAADt5povAAAAAXNSR0IArs4c6QAACmpJREFUWEfNVwl0U1Ua/u57ycuetGmatOneJt0prWUpYEVBkB0dQFkcGQRRYZwB5AyLy3gAHSgqjqgjokg944oiCiguI6ioFbpQSimFlkK3hO5p0uzv3TkJTaciwsyZOZ6557yTd/Lu/b97/+X7v0vwKw/yK+Ph/xowsLnBT8g5AgDa/1zXYdc7YQggYChg+FqD6f94TfBrAYYMBICY+CHQxMch1WBAMsSItHhBHS60e7pQZ7Wi3laF7n7A0CavusGrAQ4syJloUAzPtRVk3uBdlGgWbtGoEe0lhJzpJWjsoyCEAjz87l5YeprwVWMpir/bha/73Ruw87PTXgkYBJsDkNwnkrKSRrhWac3dcyjvlfs9QKcLtLaH+m0eCCwDuCEibqJkfIxcRMUS8IKiu6sj+kBtif6llu1vlvTHPHDwAHBwDAYMgi3NV2nnptH5eaOFVfXDnAnnJRA4P/ztHrC1Lpa1IBItJBdNfBY6fFFw+pXUB4kfrIRCJmWIXiViFeJmtqL6ec+KzS+gudk9KLYDgAEw5pmbYBytx+qCFDzUlQpUZoLvlhLSzrPsjw69UNmR333OktFgd6ic4MQM4rUGkmyMITqNXBCDgvoovELgIYRle0lL29+FxY89gro6ewh0IM2fGA79bUl4aGQM1nnDCG3PA62Mp0yrn3F9eVx2/JtDxmJrGVOGTns3XK1NQQMmk0QplSZHJedOjkkZ+luanjj0fIqUt8RJBF7GssRPeklj2+vCsg3rcPq0P+Da4MkmGiArmoA7h4TjBV4EqS+V0LpsypSKcGHvO3j64B7sRiucMA6PA8+bcan8cH84BpIiT55nNEVmLkuIzf69PS1MWTFS7aseGcH0acVWlFRuxZ2rXgxgBU94bgFGqiXkpQglzaVK8H15YEq1qC4qxprP38Cn/e7gxIaZeUSpm8aLXRX8mbc+vKIMqE6nU+Sop842q5KKYjmZtsso9laO1QvnM1QnOoqeW+o4fLiaLDUadQvT2QdGJbg28MoOgYknxJJAzz7yBf5cvBPvA2BVKqPmxtvmLJw6Y/baEQXDdA2W5q4P93/27jsvPLkFbsvFwQyk1ZoUqZHjFiRpkp5JZgin8VO4ROhpE2yvvnhs83pSkTp2eHi4d3tswqVhQlyD4IqB/bSP7hy1BusDYMCI2El3zluz5L7bl44x29HTx/McQ5kezkg3f9773Z6181bCVlYxKONJetTNcRpV6toEbfrSBJGHalgR8fL+kv11ex8jlVk33ZOp4XbQyIsSJuMctUWTktm76NLDlagJAkrGxWeNmvRo/vS5C10RBqGqRcTGaCk1GQThZEPniR82zVuB7iPfBeKDAA1c/iUPZC8pdDOq112S6ASzROBZUGuTrelrcjRrzLYCteqPft1FwZd6pu+CnO4eshErBiWFFJEb5yK2cCfyC1koCIVHALzdvbCU7Man01f3F3aIxIOJuDHOlKhUmB7tVd6wsIYJEzIlgt8nCN3k1NDC/ely1WSfxiL0mqob32r1blq5F8X9O73Mh0pDJGdYeD8S71jPJ+VwqkgOUVxrl6V0317X969t93afPHUFkZD88HDV03FJi/TylKLt3gwfOIU8SQxKmnPHVhgkihyfsktwxNdU/anKtmp3aZAPA64JABKoJpmhLXwcKXPuQnoyYRQMI2MFKvG4qNR50WLmviwu3/3YNrvd3jnIM6LKQtPMeFHEayfs6eLXiYkoRTIpaRg2/lQ8y2X4xU449BeOLa66+OC+c6gctBDQry5gwsw75Lnjs0VmHbU51Yxe6qOpkk7UtzBEkUQ702yHdh7YsuiRQTRGTszUTojyad+Qd6VqD/sNfftpHMi6YQ+Xz+DsWfm0Hr2KnoolDWXL99WjfBAgo4yank5U+U+p0sdNl2cbhDq3mZWIKI2gF7uEH49YOyNuyVAMlZV6d81Y7mw6VtbvHXryXtwW7da/EdGYrfP7ON4J4iVTctaW5Ck1+TNR600Qztc9bq1Zs+NC++f9gMFemHdv8USX2/Dq+eaoaK85FdBKAIEKcF+qx6F1r4IkhkNfMB3tHz2LczsC8ScmE0TvTcRvMhnNLrY6Uyo4tJRhfYSMz/zDnhhl/B154j6+kD9rrb1UtnVBw5kgDV2OYaxUfNebc8AlvULrLRI+KoYiKRoEVAB/qZ4c2bqBP/Hch4BUD4gdQDCOzM35CH90BO67RaN40ldqBrHFgLC8QG5MW7bJoEpar2N5ZIqdzhTX6bemlb2/HECAbAODw5SjsyDSF6OpUUQ0OtCMbAqOoXBaK3Bw/gq0Hvl+kAQJlsXfFiNjiI48NUrMTfWVJQukPdntoW4LmZCx8g6pJOI1jmXCYiUiIZJ4Th6q/2DVUeuJf2Vq5O+GgjrmQVD1MQmz7gu/cWyMMVFCu9s6jze/PHU5bOUBpgkVPjEB4veKMM2kILvkDSKlUJdAXc2mC9/2WvaRkUn35Khk+i1qqWEiQ7xCDMd6xbxjz9PHNj2IQFO/PIIdWz/77dF5QxJemTIpP7Ozo8/n77tUVrRy8cP+lu8Hd3dmw0pkjDBiywQNmcSfYASmw0hcDRlfza8pXUF0ujRVRtTku7WymO2Mxw0pyyKMo229zvrn36zatTlEVQFQpSFFN+butUuih83Y0OnVMFG89dDOe4cuAGw9l3kXdNw0RM25FStnpWGVthwCbSFwuxXWqpMxfx1dWrs16G/lxNWZjDziL1qJYWpsaztvcPBMGPW3tjtqtn1c9/bz/RwZMIi8yfenRg4t2GDIGjbSWvLZzi9eXF0EwBeYkzMZsZOmYcX04ViRexZEfgrgbRA8DP4x5QAWfXsR1lDHF2HBtluhitghgig2vMfOx3a5GaPd2+vurP+o+sKXW63euuqQENJqtWqn0xnudrsDrQlIhDRvlGhkwXh+zbjhdHJaB2h6FSjOg/b5Sc07FXTdgz/g4EADDi6KzFSg8O67SFTKsxSCCpTnxX6B0booI+3tbrNfOn3A1l75Cd/edArE0Q51HKDWxMuzo28wj+iYPmbI6fGjozqVei+laY2UxlYCrjbSVN5Ki276GC+H6jqk2i6fNDlfhSFT55LotE2UMhHw+QRwIkApY6FWAWEyIFzkh4Z1ctJeJoY7Jc9gDzJZOIosro+Gi8Gr+0Dya8DSalw4VoeiCQcHwIJy5GcyEYmJnCR91ljGnPk4MUeOhpEIjBw+MeeiMrGdUaOFNfhPs0a+FGH+ehrJUr9JDaoWExZiyho9jDfuW/bH99+lTz50zB9irAHtczUhHCyDnAdG62OyHfOj09uXySQ2M/F6QLw8GH+QfihlgGgFIWlhBCqZAMoQoc8uOl9bzu34oIjZXXb2J53jqkI4lBM/Ech5MxAdZsbthgxMURtIDisjBk5MuCQZhUlOPX0OamltRGXtSXxa9g0+Of4NAhLyF+8X17rMXLmIRGZCIZXBwBCoFYFa8MDWY0VbezscVyq4X7q+Xe+6FrAT1CiDZMRgT4TeQ3NCMuNqc4L//TuAV7p6cGaHkmEgRr+IdIUGud68/9n3//SE/zXwrw74T3XSTDJjBhdXAAAAAElFTkSuQmCC',
        caption             :   str =   (None),
        reply_to_message_id :   str =   (None)
        ) -> (
            dict or ...
            ):
            
            '''
            self.send_gif('chat-id', 'path/file', 100, 100)
            '''
            
            uresponse: list = UserMethods.upload_file(self, file)
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'sendMessage',
                    auth        =   self.auth,
                    data        =   {
                        'object_guid'           :   chat_id,
                        'is_mute'               :   False,
                        'rnd'                   :   str(randint(100000,999999999)),
                        'file_inline'           :   {
                            'access_hash_rec'   :   uresponse[1],
                            'dc_id'             :   uresponse[0]['dc_id'],
                            'file_id'           :   str(uresponse[0]['id']),
                            'auto_play'         :   False,
                            'file_name'         :   file.split('/')[-1],
                            'width'             :   width,
                            'height'            :   height,
                            'mime'              :   file.split('.')[-1],
                            'size'              :   str(len(get(file).content if 'http' in file else open(file, 'rb').read())),
                            'thumb_inline'      :   thumbnail,
                            'type'              :   'Gif'
                        },
                        'text'                  :   caption,
                        'reply_to_message_id'   :   reply_to_message_id
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'rubx'
                )
            )

    def update_profile(
        self        :   'Client',
        **kwargs    :   str
        ) -> (
            dict
            or
            ...
            ):

            '''
            `self.update_profile(username='username')`
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '4',
                    method      =   'updateUsername' if 'username' in list(kwargs.keys()) else 'updateProfile',
                    auth        =   self.auth,
                    data        =   {
                        'username'   if 'username'   in list(kwargs.keys()) else None     :   kwargs.get('username')   or None,
                        'first_name' if 'first_name' in list(kwargs.keys()) else None     :   kwargs.get('first_name') or None,
                        'last_name'  if 'last_name'  in list(kwargs.keys()) else None     :   kwargs.get('last_name')  or None,
                        'bio'        if 'last_name'  in list(kwargs.keys()) else None     :   kwargs.get('bio')        or None,
                        'updated_parameters'                                              :   list(kwargs.keys())
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'android'
                    
                )
            )

    def get_avatars(
        self    :   Client,
        chat_id :   str
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            self.get_avatars('your-guid')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getAvatars',
                    data        =   {
                        'object_guid'   :   chat_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def delete_avatar(
        self        :   Client,
        chat_id     :   str,
        avatar_id   :   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.delete_avatar('your-guid', 'id')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'deleteAvatar',
                    auth        =   self.auth,
                    data        =   {
                        'object_guid'   :   chat_id,
                        'avatar_id'     :   avatar_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def get_file(
        self            :   Client,
        download_type   :   str     =   'message' or 'my_inserts',
        save            :   bool    =   False,
        **kwargs        :   str or dict
        ) -> (
            dict or ...
            ):

            '''
            self.get_file('message', True, save_as='file.*', chat_id='chat-guid', message='msgid')
            '''

            result: bytes = b''

            if (download_type == 'message'):
                
                message: str or dict = kwargs.get('message')

                if type(message) != dict:
                    message: dict = UserMethods(auth=self.auth, banner=False, creator_channel_open=False).get_messages_by_id(kwargs.get('chat_id'), [str(message)])[0]

                file_id, size, dc_id, access_hash_rec, file_name = str(message['file_inline']['file_id']), message['file_inline']['size'], str(message['file_inline']['dc_id']), message['file_inline']['access_hash_rec'], message['file_inline']['file_name']

            else:
                file_id, size, dc_id, access_hash_rec, file_name = str(kwargs['file_id']), kwargs['size'], str(kwargs['dc_id']), kwargs['access_hash_rec']
            
            header: dict = {
                'auth'              :   self.auth,
                'file-id'           :   file_id,
                'access-hash-rec'   :   access_hash_rec
            }

            server: str = f'https://messenger{dc_id}.iranlms.ir/GetFile.ashx'

            if size <= 131072:

                header['start-index'], header['last-index'] = '0', str(size)
                
                while 1:

                    try:
                        result += get(url=server, headers=header).content
                        break
                    except Exception:
                        continue

            else:

                while 1:

                    try:
                        if 0 <= 131072:
                            header['start-index'], header['last-index'] = '0', str(size)
                            result += get(url=server, headers=header).content
                        
                        else:
                            for i in range(0, size, 131072):
                                header['start-index'], header['last-index'] = str(i), str(i+131072 if i+131072 <= size else size)
                                result += get(url=server, headers=header).content
                        break

                    except Exception:
                        continue
                    
            if save:

                open(kwargs.get('save_as') or f'{file_name}', 'wb+').write(result)

                return {
                    'status'    :   'saved',
                    'file_name' :   kwargs.get('save_as') or file_name
                    }

            else:
                return result

    def method(name: str, types: str, **data) -> dict or ...:
        
        import os
        methods: dict = __import__('json').load(open(os.path.join(os.path.dirname(os.getcwd()), 'methods.json')))
        
        def params(
            **kwargs
            ) -> dict:
            
            data: dict = methods.get(types).get(name).get('params')
            
            map(lambda key: data.update({key: kwargs.get(key)}, list(kwargs.keys())))
            
            return Method.from_json(name, data=data)

        return params(data)

    def set_setting(
        self    :   Client,
        **kwargs:   dict or str
        ) -> (
            dict or ...
            ):

        '''
        for type setSetting: Nobody, MyContacts, Everybody
        
        USE:
            self.set_setting(show_my_last_online='Nobody')
        
        PARAMS:
            show_my_last_online, show_my_phone_number, show_my_profile_photo, link_forward_message, can_join_chat_by
        '''

        return (
            GetData.api(
                version     =   self.api_version or '5',
                method      =   'setSetting',
                auth        =   self.auth,
                data        =   {
                    'settings'          :   kwargs,
                    'update_parameters' :   list(kwargs.keys())
                    },
                mode        =   self.city,
                proxy       =   self.proxy,
                platform    =   self.platform or 'web'
            )
        )

    def create_poll(
        self    :   Client,
        **kwargs:   str or dict
        ) -> (
            dict or ...
            ):

            '''
            self.send_poll(...)
            '''

            return (GetData.api(version=self.api_version or '4', method='createPoll', auth=self.auth, data=kwargs, mode=self.city, proxy=self.proxy, platform=self.platform or 'android'))

    def vote_poll(
        self            : Client,
        poll_id         : str,
        selection_index : int
        ) -> (
            dict or ...
            ):

            '''
            self.votte_poll('poll-id', '1')
            '''

            return (GetData.api(version=self.api_version or '4', auth=self.auth, method='votePoll', data={'poll_id': poll_id, 'selection_index': selection_index}, proxy=self.proxy, platform=self.platform or 'android', mode=self.city))

    def delete_chat_history(
        self            :   'Client',
        chat_id         :   str,
        last_message_id :   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.deleteChatHistory('chat-guid', '0')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'deleteChatHistory',
                    auth        =   self.auth,
                    data        =   {
                        'object_guid'       :   chat_id,
                        'last_message_id'   :   last_message_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def search_global_objects(
        self        :   Client,
        search_text :  str
        )-> (
            dict or ...
            ):

            '''
            self.search_global_objects('Hey')
            '''

            return (
                GetData.api(
                    version     =   self.api_vesion or '5',
                    method      =   'searchGlobalObjects',
                    auth        =   self.auth,
                    data        =   {
                        'search_text'   :   search_text
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def get_poll_status(
        self    :   'Client',
        poll_id :   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_poll_status('id')
            '''
            
            return (
                GetData.api(
                    version     =    self.api_version or '5',
                    auth        =    self.auth,
                    method      =   'getPollStatus',
                    data        =   {
                        'poll_id'   :   poll_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def get_poll_option_voters(
        self            :   Client,
        poll_id         :   str,
        selection_index :   str,
        start_id        :   str =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_poll_option_voters('id', 0)
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'getPollOptinVoters',
                    auth        =   self.auth,
                    data        =   {
                        'poll_id'           :   poll_id,
                        'selection_index'   :   selection_index,
                        'start_id'          :   start_id
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def report_object(
        self                :   Client,
        chat_id             :   str,
        report_description  :   str =   None,
        report_type         :   str =   100,
        report_type_object  :   str =   None,
        message_id          :   str =   None,
        ) -> (
            dict or ...
            ):

            '''
            `self.report_object('chat-guid', 'spam')`
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '4',
                    method      =   'reportObject',
                    auth        =   self.auth,
                    data        =   {
                        'object_guid'           :   chat_id,
                        'report_description'    :   report_description, 
                        'report_type_object'    :   Scanner.check_type(chat_id) if report_type_object else 'Object', 
                        'report_type'           :   report_type,
                        'meesage_id'            :   message_id
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'android'
                    )
                )

    def get_link_from_app_url(
        self   : Client,
        app_url: str
        ) -> (
            dict or ...
            ):
            
            '''
            this method for open link on rubika and info link
            
            self.get_link_from_app_url('https://rubika.ir/channel/*')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getLinkFromAppUrl',
                    data        =   {
                        'app_url'   :   app_url
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def send_chat_activity(
        self    :   Client,
        chat_id :   str,
        activity:   str =   'rubx-lib'
        ) -> (
            dict or ...
            ):
            
            '''
            self.send_chat_activity('chat-guid', is typing...')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendChatActivity',
                    data        =   {
                        'object_guid'   :   chat_id,
                        'activity'      :   activity
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def add_address_book(
        self        :   Client,
        phone       :   str,
        first_name  :   str =   None,
        last_name   :   str =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.add_address_book('09...', 'contact', 'my love')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'addAddressBook',
                    data        =   {
                        'phone'     :   phone,
                        'first_name':   first_name,
                        'last_name' :   last_name
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def delete_user_chat(
        self                    :   Client,
        chat_id                 :   str,
        last_deleted_message_id :   str
        ) -> (
            dict or ...
            ):
            
            '''
            `self.delete_user_chat('chat-guid', '0')`
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'deleteUserChat',
                    data        =   {
                        'user_guid'                 :   chat_id,
                        'last_deleted_message_id'   :   last_deleted_message_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def search_globl_messages(
        self        :   Client,
        search_text :   str,
        types       :   str =   'Text',
        start_id    :   str =   '0'
        ) -> (
            dict or ...
            ):
            
            '''
            this method for search text in messages
            
            
            USE:
            
                self.search_global_messages('hi')
                
            PARAMS:
            
                1- self is a self object
                2- search_text is a text for searching
                3- type is a format action for types: Text, Photo, Gif, ...
                4- start_id is next chats
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'searchGlobalMessages',
                    data        =   {
                        'search_text'   :   search_text,
                        'type'          :   types,
                        'start_id'      :   start_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def get_contacts_last_online(
        self        :   Client,
        chat_ids    :   list    =   None,
        usernames   :   list    =   None
        ) -> (
            dict
            ):
            
            '''
            self.get_contacts_last_online(['u0...', ])
            '''
            
            if usernames:
                with Client(self.auth, banner=False) as client:
                    chat_ids: list = [client.get_object_by_username(username)['chat']['object_guid'] for username in usernames]

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getContactsLastOnline',
                    data        =   {
                        'user_guds' :   chat_ids
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def get_abs_objects(
        self        :   Client,
        chat_ids    :   list    =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_abs_objects(['u0...', ])
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getAbsObjects',
                    data        =   {
                        'objects' :   chat_ids
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def get_messages_updates(
        self    :   Client,
        chat_id :   str,
        state   :   typing.Union[int, str] =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_messages_updates('chat-guid')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getMessagesUpdates',
                    data        =   {
                        'object_guid'   :   chat_id,
                        'state'         :   state or str(round(datetime.datetime.today().timestamp()) - 250)
                      },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )
    
    def send_mention(
        self                :   Client,
        chat_id             :   str,
        text                :   str,
        user_guid           :   str,
        mode                :   str =   'User',
        reply_to_message_id :   str =   None
        ) -> (dict or ...):
        
        '''
        self.send_mention('chat-guid', 'hi', 'u0...')
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    data        =   {
                        'object_guid': chat_id,
                        'rnd': str(randint(100000,999999999)),
                        'text': text,
                        'reply_to_message_id': reply_to_message_id,
                        'metadata': {
                            'meta_data_parts':[
                                {
                                'type': 'MentionText',
                                'mention_text_object_guid': user_guid,
                                'from_index': 0,
                                'length': len(text),
                                'mention_text_object_type': mode
                                }
                                ]
                            }
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def mention_text(
        self                :   'Client',
        chat_id             :   'str',
        user_guids          :   'list[str]',
        text                :   'str',
        reply_to_message_id :   'str'   =   None
        ) -> (dict or ...):

        '''
        self.mention_text('chat-guid', ['u0...'], '@hi@...')
        '''

        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    data        =   {'object_guid': chat_id, 'rnd': str(randint(100000,999999999)), 'reply_to_message_id': reply_to_message_id}.update({'text': Tags.checker(text, user_guids)[1], 'metadata': {'meta_data_parts': Tags.checker(text)[0]}}),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def add_folder(self: Client, name: str, **kwargs) -> (dict or ...):
        
        '''
        this method for adding folders in account
        
        USE:
            self.add_folder('name', include_chat_types = ['Contacts', ])
        
        PARAMS:
            1- self is a self object
            2- name is folder name
            3- kwargs is: include_chat_types = ['Contacts', ...], ... include_chat_types: list, exclude_chat_types=None, include_object_guids=None, exclude_object_guids=None
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'addFolder',
                    data        =   {
                        'name'          :   name,
                        'is_add_to_top' :   'true'
                        }.update(kwargs),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def send_messag_api_call(
        self        :   Client,
        text        :   str,
        button_id   :   str,
        message_id  :   str,
        chat_id     :   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.send_message_api_call(text='text', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='newtextq_5f0069d7108cd24b2a958dad', message_id='7665754757')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessageAPICall',
                    data        =   {
                        'text'          :   text,
                        'object_guid'   :   chat_id,
                        'message_id'    :   message_id,
                        'aux_data'      :   {
                            'button_id' :   button_id
                            }
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def report_to_rubika_admin(
        self        :   Client,
        report_text :   str
        ) -> (dict):

        '''
        this method for send report to @supportbot
        '''

        def event(*args):
            with StartClient(self.auth) as client:
                client.send_message(text='/start', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7')
                sleep(0.5)
                client.send_message(text='سؤال دارم', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='question')
                sleep(0.5)
                get: list = client.get_messages_interval('b0Y0a2cafbaf668e282d2dc02a1fe2a7', str(client.get_chat_info('b0Y0a2cafbaf668e282d2dc02a1fe2a7')['data']['chat']['last_message_id']))['data']['messages']
                client.send_messag_api_call(text='گزارش محتوای خلاف قوانین', object_guid='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='faq_5f0069d7108cd24b2a958dad', message_id=str(get[int(len(get)-1)]['message_id']))
                sleep(0.5)
                get: list = client.get_messages_interval('b0Y0a2cafbaf668e282d2dc02a1fe2a7', str(client.get_chat_info('b0Y0a2cafbaf668e282d2dc02a1fe2a7')['data']['chat']['last_message_id']))['data']['messages']
                client.send_messag_api_call(text=report_text, object_guid='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='newtextq_5f0069d7108cd24b2a958dad', message_id=str(get[int(len(get)-1)]['message_id']))
                return {'send_report_to': 'supportbot', 'sended': True, 'report_text': report_text, 'sended_by':'rubx_lib'}

        return event() # TODO: use the thread

    def send_movie(
        self,
        chat_id             :   str,
        file                :   str,
        height              :   typing.Union[int, str]  =   720,
        width               :   typing.Union[int, str]  =   720,
        reply_to_message_id :   str                     =   None,
        is_mute             :   bool                    =   False,
        auto_play           :   bool                    =   False,
        caption             :   str                     =   None,
        metadata            :   dict                    =   None,
        parse_mode          :   str                     =   None
        ) -> (dict):
        
        '''
        `self.send_movie('chat-guid', 'vid.mp4')`
        '''

        uresponse: list = UserMethods.upload_file(self, file)

        data: dict = {
            'file_inline'           :   {
                'access_hash_rec'   :  uresponse[1],
                'auto_play'         :   auto_play,
                'dc_id'             :   uresponse[0]['dc_id'],
                'file_id'           :   str(uresponse[0]['id']),
                'file_name'         :   file.split('/')[-1],
                'height'            :   height,
                'mime'              :   file.split('.')[-1],
                'size'              :   str(len(get(file).content if 'http' in file else open(file, 'rb').read())),
                'thumb_inline'      :   file,
                'time'              :   round(__import__('tinytag').TinyTag.get(file).duration * 1000),
                'type'              :   'Video',
                'width'             :   width
                },
            'is_mute'               :   is_mute,
            'object_guid'           :   chat_id,
            'text'                  :   caption,
            'metadata'              :   metadata,
            'rnd'                   :   str(randint(100000,999999999)),
            'reply_to_message_id'   :   reply_to_message_id
            }

        if (parse_mode):
            base: list = UserMethods.parsation(str('HTML' if len(findall(r'(<.*?>)', text)) >= 2 else 'markdown'), text)
            data.update({'metadata': {'meta_data_parts':   base[0]}, 'text': base[1]})
            data.update({'text': base[1]})
            caption: bool = False
        
        if (caption): data.update({'text': base[1]})
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    data        =   data,
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def send_music(
        self,
        chat_id             :   str,
        file                :   str,
        time                :   str                            =   None,
        height              :   typing.Union[float, int, str]  =   0.0,
        width               :   typing.Union[float, int, str]  =   0.0,
        reply_to_message_id :   str                            =   None,
        is_mute             :   bool                           =   False,
        auto_play           :   bool                           =   False,
        caption             :   str                            =   None,
        metadata            :   dict                           =   None,
        parse_mode          :   str                            =   None
        ) -> (dict):

        '''
        `self.send_music('chat-guid', 'music.mp3')`
        '''

        from tinytag import TinyTag
        uresponse: list = UserMethods.upload_file(self, file)
        
        data: dict = {
            'file_inline'   :   {
                'access_hash_rec'   :   uresponse[1],
                'auto_play'         :   auto_play,
                'dc_id'             :   uresponse[0]['dc_id'],
                'file_id'           :   str(uresponse[0]['id']),
                'file_name'         :   file.split('/')[-1],
                'height'            :   height,
                'mime'              :   file.split('.')[-1],
                'music_performer'   :   str(TinyTag.get(file).artist),
                'size'              :   len(GET(file).content if 'http' in file else open(file, 'rb').read()),
                'time'              :   time or round(TinyTag.get(file).duration),
                'type'              :   'Music',
                'width'             :   width
                },
            'is_mute'               :   is_mute,
            'object_guid'           :   chat_id,
            'text'                  :   caption,
            'metadata'              :   metadata,
            'rnd'                   :   str(randint(100000,999999999)),
            'reply_to_message_id'   :   reply_to_message_id
            }

        if (parse_mode):
            base: list = UserMethods.parsation(str('HTML' if len(findall(r'(<.*?>)', text)) >= 2 else 'markdown'), text)
            data.update({'metadata': {'meta_data_parts':   base[0]}, 'text': base[1]})
            data.update({'text': base[1]})
            caption: bool = False
        
        if (caption): data.update({'text': base[1]})
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    data        =   data,
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def get_chat_last_message_id(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_message_id('chat-guid') # the res is last message id from a chat: '99999...'`
        '''
        
        return self.get_chat_info(chat_id).get('data').get('chat').get('last_message_id')

    def get_chat_last_text(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_text('chat-guid') # the res is last text from a chat`
        '''
        
        return self.get_chat_info(chat_id).get('data').get('chat').get('last_message').get('text')
    
    def get_chat_last_object(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_object('chat-guid') # the res is a chat guid`
        '''
        
        return self.get_chat_info(chat_id).get('data').get('chat').get('last_message').get('object_guid')

    def get_chat_first_message(self, chat_id: str) -> (dict):
        
        '''
        # TO GET FIRST MESSAGE A CHAT 
        
        `self.get_first_message('chat-guid') # the res: {'object_guid': ..., 'text': ..., 'message_id': ...,}`
        '''
        
        data: dict = self.get_messages_interval(chat_id=chat_id, middle_message_id=0).get('data').get('messages')
        
        if len(data) < 1:
            return (self.get_messages_interval(chat_id=chat_id, middle_message_id='1').get('data').get('messages')[0])
        else:
            return (data[0])

    def get_last_message(self, chat_id: str) -> (dict):
        
        '''
        `self.get_last_message('chat-guid') # the res is a dictionary from a chat: {'object_guid', ..., 'text': ..., 'message_id': ..., }`
        '''
        
        return (self.get_chat_info(chat_id).get('data').get('chat').get('last_message'))

    def chat_possession_transition(self, *args) -> (dict):
        pass

class GroupMethods:

    def __enter__(
        self    :   (
            'Client'
            )
        ):
        return (
            self
            )

    def __exit__(
        self    :   (
            'Client'
            ),
        *args,
        **kwargs
        ) -> (...):
        ...

    def ban_group_member(
        self            :   ('Client'),
        user_id         :   (str)   =   (None),
        member_username :   (str)   =   (None),
        chat_id         :   (str)   =   (None),
        link            :   (str)   =   (None),
        action          :   (str)   =   ('Set'),
        ) -> (
            dict
            ):

        '''
        self.ban_group_member(user_id='chat id or guid', chat_id='chat guid')
        
        PARAMETRS:
            1- self - self object
            2- user_id - target guid or chat id
            3- member_username - to do nt using user_id and to insert: '@username'
            4- link - to dont using chat_id and to insert: 'https://rubika.ir/+'
            5- action is actions type: 'Set', 'Unset'
        '''

        if (link):
                chat_id: str = Maker.check_link(link=link, key=self.auth)
        if (member_username):
            user_id: str = Maker.check_link(link=member_username, key=self.auth)
        
        return (
            GetData.api(
                version     =   self.api_version or '4',
                method      =   'banGroupMember',
                auth        =   self.auth,
                data        =   {
                        'group_guid'    :   chat_id,
                        'member_guid'   :   user_id,
                        'action'        :   action
                        },
                proxy       =   self.proxy,
                mode        =   self.city,
                platform    =   self.platform or 'android',
                )
            )

    def add_group_members(
        self        :   'Client',
        user_ids    :   (list)  =  (None),
        usernames   :   (list)  =   (None),
        chat_id     :   (str)   =   (None)
        ) -> (
            dict
            ):
            
            '''
            self.add_group_members(['user-guid', ], chat_id='group-guid')
            
            PARAMETERS:
                1- self object
                2- user_ids is targets guid
                3- usernames for dont using user_ids to inserts: ['@username', '@...']
                4- chat_id is group guid
               
            '''

            if (usernames):
                user_ids    :   (
                    (
                        list
                        )
                    )    =       []
                with Client(self.auth, banner=False) as app:
                    assert list(map(lambda user: user_ids.append(str(app.getObjectByUsername(user.replace('@', ''))['chat']['object_guid'])), (usernames)))

            return (
                GetData.api(
                    version='5',
                    method='addGroupMembers',
                    auth=self.auth,
                    data={
                        'group_guid'    :   chat_id,
                        'member_guids'  :   user_ids
                        },
                    mode=self.city,
                    proxy=self.proxy,
                    paltform='web',
                    )
                )

    def get_group_admin_members(
        self        :   ('Client'),
        chat_id     :   (str)   =   (None),
        username    :   (str)   =   (None),
        link        :   (str)   =   (None)
        ) -> (
            dict
            ):
            
            '''
            self.get_group_admin_members('chat guid')
            
            PARAMETERS:
                -1 self is a self object
                -2 chat_id is chat guid
                -3 username is for dont using chat_id and to insert: '@username'
                -4 link is for dont using chat_id or username and to insert: 'https://rubika.ir/'
                - END :)
            '''
            
            if (username or link):
                chat_id: str = Maker.check_link(link=username or link, key=self.auth)

            return (
                GetData.api(
                    version='5',
                    method='getGroupAdminMembers',
                    auth=self.auth,
                    data={
                        'group_guid'  :   (
                            chat_id
                            )
                        },
                    mode=self.city,
                    platform='web',
                    proxy=self.proxy
                    )
                )

    def set_group_default_access(
        self        :   ('Client'),
        access_list :   (list),
        chat_id     :   (str)   =   (None),
        username    :   (str)   =   (None),
        link        :   (str)   =   (None)
        ) -> (
            dict
            or
            ...
            ):
            
            
            '''
            from rubx import accesses
            self.set_group_default_access([accesses.SendMessages, ...], 'chat guid')
            
            PARAMETERS:
                1- self is a self object
                2- access_list is a list for users access
                3- chat_id is chat guid
                4- username is for dont using chat_id and to insert: '@username'
                5- link is for dont using chat_id or username and to insert: 'https://rubika.ir/username'
                - END :)
            '''

            if (username or link):
                chat_id: str = Maker.check_link(link=username or link, key=self.auth)
            
            return (
                GetData.api(
                    version     =   self.api_version or '4',
                    method      =   'setGroupDefaultAccess',
                    auth        =   self.auth,
                    data        =   {
                        'access_list'   :   (access_list),
                        'group_guid'    :   (chat_id)
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'android'
                    )
                )

    def get_group_all_members(
        self        :   ('Client'),
        chat_id     :   (str)   =   (None),
        start_id    :   (str)   =   (None)
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            self.get_group_all_members('chat guid')
            
            PARAMETERS:
                1- chat_id is chat guid (group type)
                2- start_id is for geting next member. and to get start_id: get key 'next_start_id'
                - END
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'getGroupAllMembers',
                    auth        =   self.auth,
                    data        =   {
                        'group_guid'    :   (chat_id),
                        'start_id'      :   (start_id)
                        },
                    proxy       =   self.proxy,
                    mode        =   self.city,
                    playform    =   self.platform or 'web'
                    )
                )

    def get_group_info(
        self    :   ('Client'),
        chat_id :   (str)   =   (None)
        ) -> (
            dict
            or
            ...
            ):

            '''
            self.get_group_info('chat guid')
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is group guid
                - END
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'getGroupInfo',
                    auth        =   self.auth,
                    data        =   {
                        'group_guid'    :   (chat_id)
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def get_group_link(
        self    :   ('Client'),
        chat_id :   (str)
        ) -> (
            str
            or
            ...
            ):
            
            '''
            self.get_group_link('group-guid')
            note: this method for admin group
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is group guid
                - END
            '''
            
            return(
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getGroupLink',
                    data        =   {
                        'group_guid'    :   (chat_id)
                    },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def set_group_link(
        self    :   ('Client'),
        chat_id :   (str)   =   (None)
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            `self.get_group_link('group-guid')`
            note: this method for admin group
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is group guid
                - END
            '''
            
            return(
                GetData.api(
                    version     =   '5',
                    auth        =   self.auth,
                    method      =   'setGroupLink',
                    data        =   {
                        'group_guid'    :   (chat_id)
                    },
                    mode        =   self.city,
                    platform    =   'web',
                    proxy       =   self.proxy
                )
            )

    def set_group_timer(
        self    :   ('Client'),
        chat_id :   (str),
        time    :   (str),
        ) -> (dict):
            
            '''
            
            ## USE:
                `self.get_group_link('group-guid')`
                
            ## NOTE:
                this method for admin group
            
            ## PARAMETERS:
                - `self` is a self object
                - `chat_id` is group guid
                - `time` is a time for group timer
            ### END
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '4',
                    method      =   'editGroupInfo',
                    auth        =   self.auth,
                    data        =   {
                        'group_guid'            :   chat_id,
                        'slow_mode'             :   time,
                        'updated_parameters'    :   ['slow_mode']
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'android'
                )
            )

    def set_group_admin(
        self            :   ('Client'),
        access_list     :   (list)  =   (None),
        chat_id         :   (str)   =   (None),
        user_id         :   (str)   =   (None),
        member_username :   (str)   =   (None),
        action          :   (str)   =   ('SetAdmin')
        ) -> (
            dict or ...
            ):

            '''
            ### note: this method for admin a member in group.
            
            ## USE:
                `from rb.Accesses import Admin`
                `self.set_group_admin([Admin.SendMessages, ...], 'group guid', 'user guid')`
            
            ## PARAMETERS:
                - `self`: is a self object
                - `access_list`: is a list for member access
                - `chat_id`: is group guid
                - `user_id`: is member guid
                - `member_username`: is member username (for dont using chat_id) and to insert: '@username'
                - `action`: is a action type. actions: 'SetAdmin', UnsetAdmin''
            '''
            
            if (member_username):
                chat_id: (str) = StartClient(self.auth, banner=False).get_object_by_username(member_username)['chat']['object_guid']

            return (
                GetData.api(
                    version     =   '5',
                    method      =   'setGroupAdmin',
                    auth        =   self.auth,
                    data        =   {
                        'group_guid'    :   chat_id,
                        'access_list'   :   access_list,
                        'action'        :   action,
                        'member_guid'   :   user_id
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   'web'
                    )
                )

    def join_group(
        self    :   ('Client'),
        link    :   (str)
        ) -> (dict):
            
            '''
            (this method for join to groups.)
            
            USE:
                self.join_group('https://rubika.ir/joing/...')
            PARAMETERS:
                1- self is a self object.
                2- link is a link rubika group.
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'joinGroup',
                    auth        =   self.auth,
                    data        =   {
                        'hash_link'   :   link.split('/')[-1]
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def group_preview_by_join_link(
        self    :   ('Client'),
        link    :   (str)
        ) -> (
            dict
            ) or (
                ...
                ):
                '''
                (this method for get group link info by join link)
                
                USE:
                    self.group_preview_by_join_link('https://rubika.ir/joing/...')
                PARAMETERS:
                    1- self is a self object.
                    2- link is a link rubika group.
                '''
                
                return (
                    GetData.api(
                        version     =   self.api_version or '5',
                        method      =   'groupPreviewByJoinLink',
                        auth        =   self.auth,
                        data        =   {
                            'hash_link'   :   link.split('/')[-1]
                            },
                        mode        =   self.city,
                        proxy       =   self.proxy,
                        platform    =   self.platform or 'web'
                    )
                )

    def leave_group(
        self    :   ('Client'),
        chat_id :   (str)
        ) -> (
            dict
            or
            ...):
            
            '''
            this method for leave the group
            
            USE:
                self.leave_group('group guid') # g0...
            PARAMETERS:
                1- self is a self oobject
                2- chat_id is group guid
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or ('5'),
                    method      =   'leaveGroup',
                    auth        =   self.auth,
                    data        =   {
                        'group_guid'    :   (chat_id)
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or ('web')
                )
            )

    def create_objcet_voice_chat(
        self    :   ('Client'),
        chat_id :   (str)
        ) -> (
            dict or ...
            ):

            '''
            self.start_voice_chat('chat-guid')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   f'create{Scanner.check_type(chat_id)}VoiceChat',
                    data        =   {
                        f'{Scanner.check_type(chat_id).lower()}_guid'   :   chat_id,
                        },
                    auth        =   self.auth,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web',
                    mode        =   self.city
                )
            )

    def set_object_voice_chat_setting(
        self            :   'Client',
        chat_id         :   (str),
        voice_chat_id   :   (str),
        title           :   (str)
        ) -> (
            dict or ...
            ):
            
            '''
            self.set_object_voice_chat_settin('chat-guid', 'id', 'the title')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   f'set{Scanner.check_type(chat_id)}VoiceChatSetting',
                    data        =   {
                        f'{Scanner.check_type(chat_id).lower()}_guid'   :   chat_id,
                        'voice_chat_id'                                 :   voice_chat_id,
                        'title'                                         :   title ,
                        'updated_parameters'                            :   ['title']
                    },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )

    def discard_object_voice_chat(
        self            :   'Client',
        chat_id         :   (str),
        voice_chat_id   :   (str),
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            self.discard_object_voice_chat('chat-guid', 'id')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   f'discard{Scanner.check_type(chat_id)}VoiceChat',
                    data        =   {
                        f'{Scanner.check_type(chat_id).lower()}_guid'   :   chat_id,
                        'voice_chat_id'                                 :   voice_chat_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def set_action_chat(
        self    :   Client,
        chat_id :   str,
        action  :   str
        ) -> (
            dict or ...
            ):

            '''
            USE:
                self.set_action_chat('chat-guid', 'Pin')
            PARAMS:
                1- self is a self object
                2- chat_id is chat guid
                3- action is a action type. actions: 'Mute', 'Unmute' | 'Pin', 'Unpin'
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'setActionChat',
                    data        =   {
                        'object_guid'   :   chat_id,
                        'action'        :   action
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def join_group_voice_chat(
        self            :   Client,
        chat_id         :   str,
        voice_chat_id   :   str,
        self_object_guid:   str,
        sdp_offer_data  :   str =   '''v=0\r\no=- 7025254686977085379 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111 63 103 104 9 0 8 106 105 13 110 112 113 126\r\nc=IN IP4 0.0.0.0\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=ice-ufrag:6Hy7\r\na=ice-pwd:pyrxfUF+roBFRHDy6qgiKSAp\r\na=ice-options:trickle\r\na=fingerprint:sha-256 8C:90:E9:0C:E7:A4:79:7E:BF:78:81:ED:A7:19:82:64:71:F7:21:AB:43:4F:4B:3A:4C:EB:B5:3C:6A:01:CB:13\r\na=setup:actpass\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=sendrecv\r\na=msid:LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE 00f6113c-f01a-447a-a72e-c989684b627a\r\na=rtcp-mux\r\na=rtpmap:111 opus/48000/2\r\na=rtcp-fb:111 
transport-cc\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtpmap:63 red/48000/2\r\na=fmtp:63 111/111\r\na=rtpmap:103 ISAC/16000\r\na=rtpmap:104 ISAC/32000\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:106 CN/32000\r\na=rtpmap:105 CN/16000\r\na=rtpmap:13 CN/8000\r\na=rtpmap:110 telephone-event/48000\r\na=rtpmap:112 telephone-event/32000\r\na=rtpmap:113 telephone-event/16000\r\na=rtpmap:126 telephone-event/8000\r\na=ssrc:1614457217 cname:lYBnCNdQcW/DEUj9\r\na=ssrc:1614457217 msid:LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE 00f6113c-f01a-447a-a72e-c989684b627a\r\n'''
        ) -> (
            dict or ...
            ):

            '''
            self.join_group_voice_chat('chat-guid', 'id', 'your-guid', ...)
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'joinGroupVoiceChat',
                    data        =   {
                        'chat_guid'         :   chat_id,
                        'voice_chat_id'     :   voice_chat_id,
                        'sdp_offer_data'    :   sdp_offer_data,
                        'self_object_guid'  :   self_object_guid
                    },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    get_display_as_in_group_voice_chat = lambda self, chat_id: GetData.api(version=self.api_version or '5', method='getDisplayAsInGroupVoiceChat', auth=self.auth, data={'chat_guid': chat_id}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)

    def leave_group_voice_chat(
        self            :   Client,
        chat_id         :   str,
        voice_chat_id   :   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.leave_group_voice_chat('chat-guid', 'id')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'leaveGroupVoiceChat',
                    data        =   {
                        'chat_guid'     :   chat_id,
                        'voice_chat_id' :   voice_chat_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def set_group_voice_chat_setting(
        self            :   Client,
        chat_id         :   str,
        voice_chat_id   :   str,
        **kwargs        :   (dict or str)
        ) -> (
            dict or ...
            ):
            
            '''
            self.set_group_voice_chat_setting('chat-guid', 'id', title='Hey')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'setGroupVoiceChatSetting',
                    data        =   {
                        'chat_guid'     :   chat_id,
                        'voice_chat_id' :   voice_chat_id,
                        'updated_parameters'    :   list(kwargs.keys())
                        }.update(kwargs),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def edit_group_info(
        self                        :   Client,
        chat_id                     :   str,
        title                       :   str =   None,
        description                 :   str =   None,
        chat_history_for_new_members:   str =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.edit_group_info('chat-guid', 'name', 'bio')
            
            actions: Hidden, Visible
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'editGroupInfo',
                    data        =   {
                        'group_guid'        :   chat_id,
                        'title'             :   title,
                        'description'       :   description,
                        'updated_parameters':   ['title', 'description', 'chat_history_for_new_members' if chat_history_for_new_members else None]
                        }.update({'chat_history_for_new_members': chat_history_for_new_members} if chat_history_for_new_members else {}),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def get_banned_chat_members(
        self    :   Client,
        chat_id :   str,
        start_id:   str =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_banned_group_members('chat-guid') # get 'next_start_id' from respone to star_id param
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '4',
                    auth        =   self.auth,
                    method      =   f'getBanned{Scanner.check_type(chat_id)}Members',
                    data        =   {
                        f'{Scanner.check_type(chat_id).lower()}_guid'        :   chat_id,
                        }.update({'start_id' : start_id} if start_id else {}),
                    mode        =   self.city,
                    platform    =   self.platform or 'android',
                    proxy       =   self.proxy
                )
            )

    def get_group_mention_list(
        self            :   Client,
        chat_id         :   str =   None,
        search_mention  :   str =   None
        ) -> (
            dict or ...
            ):
            
            '''
            self.get_group_mention_list('chat-guid')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'getGroupMentionList',
                    data        =   {
                        'group_guid'    :   chat_id,
                        'search_mention':   search_mention
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def delete_no_access_group_chat(self: Clean,
                                    chat_id: str) -> (dict or ...):
        
        '''
        self.delete_no_access_group_chat('group-guid')
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'deleteNoAccessGroupChat',
                    data        =   {
                        'group_guid'    :   chat_id
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

class ChannelMethods:
    
    def __enter__(
        self    :   (
            'Client'
            )
        ):
        return (
            self
            )

    def __exit__(
        self    :   (
            'Client'
            ),
        *args,
        **kwargs
        ) -> (...):
        ...
    
    set_channel_link        =   lambda self, chat_id: GetData.api(version=self.api_version or '5', method='setChannelLink', auth=self.auth, data={'channel_guid': chat_id}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    check_channel_username  =   lambda self, username: GetData.api(version=self.api_version or '5', method='checkChannelUsername', auth=self.auth, data={'username': username}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    delete_channel          =   lambda self, chat_id: GetData.api(version=self.api_version or '5', method='removeChannel', auth=self.auth, data={'channel_guid': chat_id}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)

    def add_channel_members(
    
        self        :   'Client',
        user_ids    :   (list),
        chat_id     :   (str)
        ) -> (
            dict
            ):

            '''

            self.add_channel_members(['user guid', ]. chat_id='channel guid')
            
            PARAMETERS:
                1- user_ids a list user guids
                3- chat_id is channel guid
            '''

            return (GetData.api(
                version     =   self.api_version or '5',
                method      =   'addChannelMembers',
                auth        =   self.auth,
                data        =   {
                    'channel_guid'  :   chat_id,
                    'member_guids'  :   user_ids
                    },
                mode        =   self.city,
                platform    =   self.platform or 'web',
                proxy       =   self.proxy
                )
                    )
    
    def get_channel_all_members(
        self            :   ('Client'),
        chat_id         :   (str)   =   (None),
        search_text     :   (str)   =   (None),
        start_id        :   (str)   =   (None)
        ) -> (
            dict
            or
            ...
            ):
            
            '''
            self.get_channel_all_members(...)
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'getChannelAllMembers',
                    auth        =   self.auth,
                    data        =   {
                        'channel_guid'  :   chat_id,
                        'search_text'   :   search_text,
                        'start_id'      :   start_id
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )
    
    def set_channel_action(
        self    :   Client,
        chat_id :   str,
        action  :   str =   'Join'
        ) -> (
            dict or ...
            ):

            '''
            this method for join and leave channels
            
            USE:
                self.set_action_chat('chat-guid', 'Pin')
            PARAMS:
                1- self is a self object
                2- chat_id is chat guid
                3- action is a action type. actions: 'Join', 'Leave'
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'joinChannelAction',
                    data        =   {
                        'channel_guid'   :   chat_id,
                        'action'        :   action
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def add_channel(
        self            : Client,
        title           : str,
        description     : str,
        channel_type    : str   =   'Public'
        ) -> (
            dict or ...
            ):
            
            '''
            this method for create channel
            
            USE:
                self.add_channel('title', 'bio')
            PARAMS:
                1- self is a self object
                2- title is channel name
                3- description is channel bio
                4- channel_type is a action type for channel. types: 'Public', 'Private'
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'addChannel',
                    data        =   {
                        'title'         :   title,
                        'description'   :   description,
                        'channel_type'  :   channel_type
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def edit_channnel_info(
        self    :   Client,
        chat_id :   str,
        **kwargs:   dict or str
        ) -> (
            dict or ...
            ):

            '''
            USE:
                self.edit_channnel_info('chat-guid', title='name')
            PARAMS:
                sign_messages, title, description
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'editChannelInfo',
                    data        =   {
                        'updated_parameters'        :   list(kwargs.keys())
                        }.update(kwargs),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def update_channel_username(
        self    :   Client,
        chat_id :   str,
        username:   str
        ) -> (
            dict or ...
            ):
            
            '''
            self.update_channel_username('channel-guid', 'username')
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'updateChannelUsername',
                    data        =   {
                        'channel_guid'  :   chat_id,
                        'username'      :   username
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def set_channel_admin(self: Client, chat_id: str, member_guid: str,
                          access_list: list = None, action: str = 'SetAdmin') -> (dict or ...):
        
        '''
        this method is for admin and unadmin a member chat
        
        
        USE:
            self.set_channel_admin('group-guid', 'user-guid', [accesses.admin.sendMessages])
        
        PARAMS:
            1- self a is self object
            2- chat_id is group guid
            3- member_guid is a user guid
            4- access_list is for access user in group: from rub import accesses.admin or ["ChangeInfo", "ViewMembers", "ViewAdmins", "PinMessages", "SendMessages", "EditAllMessages", "DeleteGlobalAllMessages", "AddMember", "SetJoinLink"]
            5- action is action type: 'UnsetAdmin', 'SetAdmin'
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'setChannelAdmin',
                    data        =   {
                        'channel_guid'  :   chat_id,
                        'member_guid'   :   member_guid,
                        'action'        :   action,
                        'access_list'   :   access_list
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def channel_preview_by_join_link(self: Client, link: str) -> (dict):
        
        '''
        get channel info from link
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'channelPreviewByJoinLink',
                    data        =   {
                        'hash_link' :       str(link.split('/')[-1])
                      },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def join_channel_by_link(
        self: Client,
        link: str
        ) -> (dict):
        
        '''
        this method for join channel with link
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '4',
                    auth        =   self.auth,
                    method      =   'joinChannelByLink',
                    data        =   {
                        'hash_link'     :   link.split('/')[-1]
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'android',
                    proxy       =   self.proxy
                )
            )

class WebSocket(object):

    def __init__(self, session) -> (None):
        self.auth: str = session
        self.enc: Encryption = Encryption(session_id)

    def __enter__(self) -> (object):
        return self

    def __exit__(self,
                 *args, **kwargs) -> (None):
        pass

    def on_open(self, ws, api_version='4') -> (None):
        
        def handShake(*args):
            
            ws.send(
                dumps(
                    {
                        'api_version'   :   api_version,
                        'auth'          :   self.auth,
                        'method'        :   'handShake'
                        }
                    )
                )
            ws.send('{}')
        
        import _thread
        
        _thread.start_new_thread(handShake, ())

    def on_message(self, message) -> (dict):
        
        try:

            parsedMessage = loads(message)
            
            return (
                    {
                        'type'  :   parsedMessage['type'],
                        'data'  :   loads(self.enc.decrypt(parsedMessage['data_enc']))
                        }
                    )

        except KeyError:
            pass

    def handle(self, func) -> (None):
        
        def decorator():
            
            import websocket
            
            while 1:
                try:
                    
                    with websocket.connect('wss://jsocket3.iranlms.ir:80') as ws:
                        with WebSocket(self.auth) as socket:
                            socket.on_open(ws, '4')
                            
                            for (res) in [ws.recv()]:
                                func(socket.on_message(res))
                            else:
                                break
                        
                except Exception:
                    continue
        
        decorator()

class RubinoClient(object):

    def __init__(self, session: str) -> (None):
        
        from requests import session as Sn
        
        self.session, self.auth, self.url = Sn(), session, 'https://rubino12.iranlms.ir'

    def __enter__(self) -> (object):
        return self

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> (None):
        pass

    def __post(self, json: dict) -> (dict):
        
        for i in range(5):
            
            try:
                with self.session.post(
                    url=self.url,
                    json=json
                    ) as (res):
                    
                    if (res.status_code != 200):
                        continue

                    else:
                        return res.json()
                        break

            except Exception as e:
                print(e)

    def makeJson(
        self,
        method  :   str,
        data    :   dict
        ) -> (dict):

        return (
            {
                'api_version'   :   '0',
                'auth'          :   self.auth,
                'client'        :   clients.android,
                'data'          :   data,
                'method'        :   method
                }
        )

    def get_profile_list(
        self,
        limit   :   int     =   10,
        sort    :   str     =   'FromMax',
        equal   :   bool    =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getProfileList',
            {
                'equal': equal,
                'limit': limit,
                'sort' : sort,
                }
        )
        return self.__post(json=json)

    def request_follow(
        self,
        followee_id :   str,
        profile_id  :   str,
        f_type      :   str  =  'Follow'
        ) -> (dict):
        
        '''
        `f_type` is a action for follow type; and actions: `Follow` and `Unfollow`
        '''
        
        json = self.makeJson(
            'requestFollow',
            {
                'f_type'        :   'Follow',
                'followee_id'   :   followee_id,
                'profile_id'    :   profile_id
                }
            )

        return self.__post(json=json)

    def create_page(
        self, **kwargs
        ) -> (dict):
        
        '''
        `self.create_page(bio='', name='', username='', email='')`
        '''
        
        json = self.makeJson(
            'createPage',
            {**kwargs}
            )
        return self.__post(json=json)

    def update_profile(
        self,
        **kwargs
        ) -> (dict):
        
        '''
        `self.update_profile(bio='', name='', username='', email='')`
        '''
        json = self.makeJson(
            'updateProfile',
            {**kwargs}
            )
        
        return self.__post(json=json)

    def is_exist_username(
        self,
        username: str
        ) -> (dict):
        
        json = self.makeJson(
            'isExistUsername',
            {
                'username': username.replace('@','')
                }
            )
        return self.__post(json=json)

    def get_post_by_shareLink(
        self,
        share_string:   str,
        profile_id  :   str
        ) -> (dict):
        
        json = self.makeJson(
            'getPostByShareLink',
            {
                'share_string'  :   share_string,
                'profile_id'    :   profile_id
                }
            )
        return self.__post(json=json)

    def add_comment(
        self,
        text            :   str,
        post_id         :   str,
        post_profile_id :   str,
        profile_id      :   str
        ) -> (dict):
        
        json = self.makeJson(
            'addComment',
            {
                'content'           :   text,
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id,
                'rnd'               :   randint(1111111111, 9999999999),
                'profile_id'        :   profile_id
                }
            )

        return self.__post(json=json)

    def like_post_action(
        self,
        post_id         :   str,
        post_profile_id :   str,
        profile_id      :   str,
        action_type     :   str =   'Like' or 'Unlike'
        ) -> (dict):
        
        
        '''
        `action_type` is a action for post; and, actions: `Like` or `Unlike`
        '''

        json = self.makeJson(
            'likePostAction',
            {
                'action_type'       :   action_type,
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id,
                'profile_id'        :   profile_id
                }
            )

        return self.__post(json=json)

    def add_post_view_count(
        self,
        post_id         :   str,
        post_profile_id :   str
        ) -> (dict):
        
        json = self.makeJson(
            'addPostViewCount',
            {
                'post_id'           :   post_id,
                'post_profile_id'   :   post_profile_id
                }
            )
        return self.__post(json=json)

    def get_comments(self,
        post_id         :   str,
        profile_id      :   str,
        post_profile_id :   str,
        limit           :   int     =   50,
        sort            :   str     =   'FromMax',
        equal           :   bool    =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getComments',
            {
                'equal'             :   equal,
                'limit'             :   limit,
                'sort'              :   sort,
                'post_id'           :   post_id,
                'profile_id'        :   profile_id,
                'post_profile_id'   :   post_profile_id
                }
            )
        return self.__post(json=json)

    def get_recent_following_posts(
        self        :   'RubinoClient',
        profile_id  :   'str',
        limit       :   'int'   =   30,
        sort        :   'str'   =   'FromMax',
        equal       :   'bool'  =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
            'equal'         :   equal,
            'limit'         :   limit,
            'sort'          :   sort,
            'profile_id'    :   profile_id
            }
            )
        return self.__post(json=json)

    def get_profile_posts(self,
        target_profile_id   :   str,
        profile_id          :   str,
        limit               :   int     =   50,
        sort                :   str     =   'FromMax',
        equal               :   bool    =   False
        ) -> (dict):
        
        json = self.makeJson(
            'getRecentFollowingPosts',
            {
                'equal'             :   equal,
                'limit'             :   limit,
                'sort'              :   sort,
                'profile_id'        :   profile_id,
                'target_profile_id' :   target_profile_id
                }
            )
        return self.__post(json=json)

    def get_profile_stories(
        self,
        target_profile_id   :   str,
        limit               :   int =   100
        ) -> (dict):
        
        json = self.makeJson(
            'getProfileStories',
            {
                'limit'         :   limit,
                'profile_id'    :   target_profile_id
                }
            )
        return self.__post(json=json)

class EventBuilder(
    Client,
    UserMethods
    ):
    
    def __str__(self) -> (str):
        return self.jsonify(indent=2)

    def __getattr__(self, name) -> (list):
        return self.find_keys(keys=name)

    def __setitem__(self, key, value) -> (...):
        self.original_update[key] = value

    def __getitem__(self, key):
        return self.original_update[key]

    def __lts__(self, update: list) -> (list):
        for index, element in enumerate(update):
            if isinstance(element, list):
                update[index] = self.__lts__(update=element)

            elif isinstance(element, dict):
                update[index] = EventBuilder(update=element)

            else:
                update[index] = element
        return update

    def __init__(self, update: dict = None) -> (None):
        self.original_update = update

    def to_dict(self) -> (dict):
        return self.original_update

    def jsonify(self, indent=None) -> (str):
        
        result = self.original_update
        result['original_update'] = 'dict{...}'
        
        return dumps(
            result,
            indent=indent,
            ensure_ascii=False,
            default=lambda value: str(value)
            )

    def find_keys(self, keys: list,
                  original_update: str = None) -> (list):

        if original_update is None:
            original_update = self.original_update

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(original_update, dict):
            for key in keys:
                try:
                    update = original_update[key]
                    if isinstance(update, dict):
                        update = EventBuilder(update=update)

                    elif isinstance(update, list):
                        update = self.__lts__(update=update)

                    return update

                except KeyError:
                    pass
            original_update = original_update.values()

        for value in original_update:
            if isinstance(value, (dict, list)):
                try:
                    return self.find_keys(keys=keys, original_update=value)

                except AttributeError:
                    pass

        raise AttributeError(f'Struct object has no attribute {keys}')

    def guid_type(self, chat_id: str) -> str:
        if isinstance(chat_id, str):
            return Scanner.check_type(chat_id)


    def action(self):
        return self.find_keys(keys=['author_type'])

    def is_user(self):
        return self.action() == 'User'

    @property
    def type(self):
        try:
            return self.find_keys(keys=['type', 'author_type'])

        except AttributeError:
            pass

    @property
    def raw_text(self):
        try:
            return self.find_keys(keys='text')

        except AttributeError:
            pass

    @property
    def message_id(self):
        try:
            return self.find_keys(keys=['message_id',
                                        'pinned_message_id'])
        except AttributeError:
            pass

    @property
    def reply_message_id(self):
        try:
            return self.find_keys(keys='reply_to_message_id')

        except AttributeError:
            pass

    @property
    def is_group(self):
        return self.type == 'Group'

    @property
    def is_channel(self):
        return self.type == 'Channel'

    @property
    def is_private(self):
        return self.type == 'User'
    
    @property
    def is_bot(self):
        return self.type == 'Bot'
    
    def is_service(self):
        return self.type == 'Service'
    
    @property
    def object_guid(self):
        try:
            return self.find_keys(keys=['group_guid', 'object_guid',
                                        'channel_guid', 'user_guid',
                                        'bot_guid', 'service_guid'])
        except AttributeError:
            pass

    @property
    def author(self):
        try:
            return self.find_keys(keys=['author_object_guid'])

        except AttributeError:
            pass
        
    @property
    def author_guid(self):
        try:
            return self.author_object_guid

        except AttributeError:
            pass
    
    def finder(self, filters) -> (object):
        
        if 'group_guid' in filters:
            return self.group_guid
        elif 'channel_guid' in filters:
            return self.channel_guid
        elif 'user_guid' in filters:
            return self.user_guid
        elif 'object_guid' in filters:
            return self.object_guid
        else:
            return self.author_object_guid
    
    def is_personl(self, chat_id: str) -> (bool):
        if isinstance(chat_id, str):
            return Scanner.check_type(chat_id) == 'User'

    def is_group(self, chat_id: str) -> (bool):
        if isinstance(chat_id, str):
            return Scanner.check_type(chat_id) == 'Group'
    
    def is_channel(self, chat_id: str) -> (bool):
        if isinstance(chat_id, str):
            return Scanner.check_type(chat_id) == 'Channel'
    
    def pin(self, chat_id: str,
            message_id: str) -> (dict):

        return self.set_pin_message(chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message_id = message or self.message_id, action='Pin')
    
    def unpin(self, chat_id: str,
              message_id: str) -> (dict):
        
        return self.set_pin_message(chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message_id = message or self.meesage_id, action='Unpin')

    def seen(self, chat_id: str,
             message: str) -> (dict):
        return self.seen_chats({chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']): message or self.self.message_id})
    
    def reply(self, **kwargs) -> (dict):
        from rb import StartClient
        return StartClient(self.auth).send_message(**kwargs)
    
    def respond(self, text: str, action: str = 'author_object_guid') -> (dict):
        from rb import StartClient
        return StartClient(self.auth).send_message(text, self.finder(action), reply_to_message_id=self.message_id)
    
    def edit(self, text: str, chat_id: str = None,
             message: str = None, action: str = 'author_object_guid') -> (dict):

        from rb import StartClient
        return StartClient(self.auth).edit_message(message_id = message or self.message_id, text=text, chat_id = chat_id or self.finder(action))
    
    def forwards(self, to: str,
                 _from: str = None, messages: list = None) -> (dict):
        
        from rb import StartClient
        return StartClient(self.auth).forward_messages(_from or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), messages or [self.message_id], to)
    
    def download(self, chat_id: str,
                 message: str, name: str) -> (dict):
        
        from rb import StartClient
        return StartClient(self.auth).get_file('message', True, saveAS='name', chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message_id= message or self.find_keys(keys=['messaage_id']))

    def delete(self, chat_id: str,
               messages: list) -> (dict):
        
        from rb import StartClient
        StartClient(self.auth).delete_messages(messages or [self.message_id], chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']))

class NewMessage(EventBuilder):
    
    def __init__(
        self,
        func        :   object,
        filters     :   list  =   None,
        pattern     :   str   =   None,
        commands    :   dict  =   None, 
        gets        :   tuple =   None,
        handle_name :   str   =   'handshake',
        ) -> (None):
        
        '''
        ## PARAMS:
            - `filters  = ['u0...', ]`
            - `pattern  = '(?) hi \S+'`
            - `commands = {'/start': 'Hey!'}`
            - `gets     = ('/start', '/info')`
        '''

        super().__init__(func, filters, pattern, commands, gets, handle_name)
        self.pattern, self.filters, self.gets, self.handle_name, self.commands, self.func = pattern, filters, gets, handle_name, commands, func
    
    @property
    def reg(self) -> (typing.Union[dict, None]):
        
        if not isinstance(self.filters, list):
            self.filters: list = [self.filters]
        
        for message in self.func(self.handle_name, get_messages=True, chat_ids=self.filters):
            
            if self.pattern:
                if not isinstance(self.pattern, str):
                    raise ValueError('oh pattern param is not string type.')
                if search(r'%s' % self.pattern, message.get('text') or message):
                    return message
            
            elif self.commands:
                
                if not isinstance(self.commands, dict):
                    raise ValueError('oh commands param is not dictionary type.')
                    
                if any(cmd in message.get('text') for cmd in list(self.commands.keys())):
                    return ([self.commands.get(cmd) for cmd in list(self.commands.keys()) if cmd in message], message)

            elif self.gets:
                
                if not isinstance(self.gets, tuple) or isinstance(self.gets, list):
                    raise ValueError('oh gets param is not a tuple or list type.')
                
                if any(cmd in message for cmd in self.gets):
                    return message

            else:
                return message

class Handler(
    Client
    ):
    
    def __init__(self, *args) -> (None):
        super().__init__(*args)
    
    def __enter__(self):
        return self

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> (None):
        pass
    
    def __appender(self, msg_id: str = None, action: str = 'edit'):
        
        if action == 'edit':
            if not msg_id in open(self.auth+'-ids.sty', 'r').read().split('\n'):
                open(self.auth+'-ids.sty', 'a+').write(msg_id+'\n')
        else:
            open(self.auth+'-ids.sty', 'w')
    
    def handle(self, method: str = 'ChatsUpdates', get_chats: bool = True,
               get_messages: bool = True, chat_ids: str = None,
               author_guid: str = None, pattern: typing.Union[tuple, list] = None) -> (dict):
        
        '''
        `method`: methods: `ChatsUpdates`, `MessagesUpdates`, `HandShake`
        `get_chats`: the chat updates
        `get_messages`: the message updates
        `chat_ids`: chat filter
        `author_guid`: author_filter
        `pattern`: the pattern is for get message filter: `('^\w{1}start', 'Hey! from rubx lib')`
        '''
        
        if ('handshake' in method.lower()):
            
            try:
                for msg in self.hand_shake():
                    if msg.get('type') == 'messenger':
                        res: dict = msg.get('data')
                        
                        if get_chats and get_messages:
                            yield res

                        elif get_messages:
                            for i in res.get('message_updates'):
                                yield res

                        elif get_chats:

                            for i in res.get('chat_updates'):
                                yield i
            except Exception:
                ...

        elif ('chatsupdates' in method.lower()):
            
            from rb import StartClient # TODO: use __init__
            
            while 1:
                
                try:
                    for msg in StartClient(self.auth).get_chats_updates().get('data').get('chats'):
                        
                        if not msg.get('last_message').get('message_id') in open(self.auth+'-ids.sty', 'r').read().split('\n'):
                            
                            if chat_ids:
                                
                                if not isinstance(chat_ids, list):
                                    chat_ids: list = [chat_ids]
                                    
                                if msg.get('last_message').get('object_guid') in chat_ids or msg.get('last_message').get('author_object_guid') in chat_ids:
                                    
                                    if pattern:
                                        if search(pattern[0], msg.get('last_message').get('text')):
                                            
                                            msg.update(msg.get('last_message'))
                                            msg.update(msg.get('abs_object') or {})
                                            del msg['last_message']
                                            del msg['abs_object']
                                            msg.update({'pattern': pattern[1]})
                                            
                                            yield msg
                                    else:
                                        
                                        msg.update(msg.get('last_message'))
                                        msg.update(msg.get('abs_object') or {})
                                        del msg['last_message']
                                        del msg['abs_object']
                                        
                                        yield msg
                            else:
                                
                                if pattern and isinstance(pattern, tuple) or isinstance(pattern, list):
                                    if search(pattern[0], msg.get('last_message').get('text')):
                                        
                                        msg.update(msg.get('last_message'))
                                        msg.update(msg.get('abs_object') or {})
                                        msg.update({'pattern': pattern[1]})
                                        del msg['last_message']
                                        del msg['abs_object']
                                        
                                        yield msg
                                else:
                                    
                                    msg.update(msg.get('last_message'))
                                    msg.update(msg.get('abs_object') or {})
                                    del msg['last_message']
                                    del msg['abs_object']
                                    
                                    yield msg
                            
                        self.__appender(msg.get('last_message').get('message_id'), 'edit')
                except Exception:
                    ...
                    
        elif ('messagesupdates' in method.lower()):
            
            from rb import StartClient
            
            while 1:
                
                try:
                    if chat_ids:
                        
                        if not isinstance(chat_ids, list):
                            chat_ids: list = [chat_ids]
                            
                        for chat_id in chat_ids:
                            for msg in StartClient(self.auth).get_messages_updates(chat_id).get('data').get('updated_messages'):
                                if not msg.get('last_message').get('message_id') in open(self.auth+'-ids.sty', 'r').read().split('\n'):
                                    
                                    if pattern and isinstance(pattern, tuple) or isinstance(pattern, list):
                                        if search('%s' % pattern[0], msg.get('last_message').get('text')):
                                            yield [msg.get('last_message'), pattern[1]]
                                    else:
                                        yield msg.get('last_message')
                                
                                self.__appender(msg.get('last_message').get('message_id'), 'edit')
                except Exception:
                    ...

    def hand_shake(self) -> (dict):
        
        while 1:
            
            @WebSocket(self.auth).handle
            def update(message):
                yield message # TODO: if len(str(message)) != 33 

    def handler(self, builder: object) -> (typing.Union[object,
                                                        iter, None]):
        
        '''
        ## EXAMPLE:
            
            from rb import Handler, NewMessage, EventBuilder, StartClient

            client = Handler(...)
            
            # the funcs: `ChatsUpdates`, `MessagesUpdates`, `HandShake` # websocket
            
            client.add_event_handling(func='HandShake', events=dict(get_messages=True, get_chats=True))
            
            @client.handler
            def update(app: StartClient, message: EventBuilder, event):
                ...
        
        '''
        
        def decorator():
            
            from rb import StartClient # __init__
            
            methods = StartClient(self.auth)
            update = Handler(self.auth)
            
            if self.handling.get('events'):
                if not isinstance(self.handling['events'], dict):
                    self.handling.update({'events': dict(get_messages=True, get_chats=True)})
            else:
                self.handling.update({'events': dict(get_messages=True, get_chats=True)})
            if not self.handling.get('func') and isinstance(self.handling.get('func'), str) and self.handling.get('func').lower() in ['handshake', 'chatsupdates', 'messagesupdates']:
                self.handling.update({'func': 'chatsupdates'})
            
            for (event) in (update.handle(method=self.handling.get('func'), **self.handling.get('events') or {})):
                event.update({'auth': self.auth})
                message = EventBuilder(event)
                builder(methods, message, event)
        
        self.__appender(action='create')
        
        while 1:
            try:
                decorator() # TODO: use the threading
            except Exception:
                pass
    
    def on(self, event) -> (typing.Union[object, None]):
        
        '''
        ## EXAMPLE:
            from rb import Handler, NewMessage
            
            client = Handler(...)
            
            @client.on(NewMessage(client.handle, handle_name='handshake').reg())
            def update(message):
                ...
        
        '''
        
        def decorator(func) -> (None):
            self.add_event_handling(func=func, events=event)
            return func

        return decorator

    def add_event_handling(self, **handlers) -> (None):
        self.handling.update({'func': handlers.get('func') or handlers.get('method'), 'events': handlers.get('events')})
    
    def remove_event_handling(self, func: object):
        try:
            self.handling.pop(func)
        except KeyError:
            ...

# main class object to set all method for use.

class StartClient(
    RubikaClient,
    UserMethods,
    GroupMethods,
    ChannelMethods
    ): # TODO: add all methods
    pass