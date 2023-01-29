#!/bin/python
# `beta` version
# main object

import os, sys

if __name__ == '__main__' and  __package__ == None or __package__ == '':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    import tinytag, Crypto
except ModuleNotFoundError:
    from .extensions import PyPi
    PyPi().installation(['tinytag', 'pycryptodome'])

import logging, platform, typing, difflib, inspect

from datetime           import  datetime
from json               import  dumps, loads
from random             import  choice, randint, sample
from re                 import  findall, search, sub, compile
from time               import  sleep, gmtime, localtime
from warnings           import  warn
from requests           import  get, post, session
from .exceptions        import  *
from .extensions        import  *
from .events            import  *
from .crypto            import  Encryption
from .connection        import  GetData, Urls, Connection, Make
from .storage           import  SQLiteSession
from .clients           import  *
from .UserMethods       import  UserMethods
from .GroupMethods      import  GroupMethods
from .ChannelMethods    import  ChannelMethods
from .rubino            import  RubinoClient
from .methods           import  Method
from .parser            import  (
    MessageEmpty, MessageEntityBold, MessageEntityCode,
    MessageEntityItalic, MessageEntityHashtag, MessageEntityMention,
    MessageEntityMentionName, MessageEntityPre, MessageEntityStrike,
    MessageEntityTextUrl, MessageEntityUnderline, MessageEntityUnknown,
    MessageEntityUrl, Metas, Tags, MetaDataLoader, MarkDown
    )

if typing.TYPE_CHECKING:
    from . import RubikaClient, UserMethods

try:
    from . import __file__ as base_file
    from . import __name__ as base_log
    from . import __package__ as base_pkg

except ImportError:
    base_file, base_log, base_pkg = locals().get('__file__') or __doc__, locals().get('__name__'), locals().get('__package__')

__all__ = [
    'Client',
    'RubikaClient',
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
    __version__ =   '10.4.6'
    __author__  =   'saleh'
    __lisense__ =   'MIT'
    __module__  =   'rubx'


__version__ = Version.__version__


class RubikaClient(object):
    
    __base_class__ = 'RubikaClient'
    
    def __str__(self, *args) -> (str):
        return dumps({'session': SQLiteSession(self.auth).information()}, indent=2) if self.auth else dumps({'__all__': __all__}, indent=2)

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
        api_client          :   (str)                               =   (None),
        return_data_an_dict :   (bool)                              =   (True),
        *args,
        **kwargs
        ) -> (None):
        
        '''
        # the main class
        ### inserts
        
        ## IMPORT:
            - from rb import RubikaClient

        ## USE:
        
            `client = RubikaClient('session-key', 'u0...', 'username', 'rubx', your_name='saleh', banner=True, creator_channel_open=True, platform='rubx', api_version='5', timeout=5, proxy={'socks5':'http://127.0.0.1:9050'}, headers={'user-agent':...}, api_client='https://messengerg56c.iranlms.ir:80', ...)`

        ## EXAMPLES:
            
            `with RubikaClient(...) as client:`
                `client.send_message(...)`
            
            # ... or ...
            
            `client = RubikaClient()`
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
            - 21 - `return_data_an_dict`: return the json data to str(ordered with dumps) or dict(normal)
        
        
        ## `what is [guid]?` : guide unique identifier | chat id : group guid, channel guid and others ...
        ## `what is [session_key] or [auth]?`: is your session id (api key) for account.
        
        ### END
        '''
        
        (self.app, self.proxy, self.enc,
            self.city, self.platform, self.api_version,
            self.headers, self.username, self.chat_id,
            self.handling, self.phone, _log,
            self.timeout, self.lang_code, self.device,
            self.check_session, self.api_client) = (app, proxy, Encryption(session_key),
                                                    city, platform, api_version,
                                                    headers, username, chat_id,
                                                    {}, phone_number, logging.getLogger(__name__),
                                                    timeout, lang_code, device,
                                                    check_session, api_client)
        
        Infos.citys.append(city)
        Infos.proxys.append(proxy)
        GetData.url: str = (api_client) # TODO: set other params 
        # TODO: set all params in __init__ object
        if banner:
            assert list(map(lambda character: (print(character, flush=True, end=''), sleep(0.01)), f'\n\033[0m< \033[31mrubx \033[0m> \033[36m | \033[31mstarted in \033[0m{str(datetime.datetime.now())}\033[31m| \033[0m{Version.__version__}\n'))
        
        if your_name:
            open('session_info.sty', 'w+').write('name: '+your_name+'\ntime started: '+str(datetime.datetime.now())+f'\key: {session_key}'+'\nyour ip: '+str(get('https://api.ipify.org').text))
        
        if session_key:
            self.auth: (str) = (session_key)
            Infos.auth_.append(session_key)
        
        elif phone_number:
            Login.SignIn(phone_number)
            
        else:
            warn('SessionWarning: please insert session key or phone_number in object')
            
        if creator_channel_open:
            # self.join_channel_action
            # import webbrowser
            pass

        if (app == 'rubx'):

            try:
                open(f'{session_key}.sty', 'r')
            except FileNotFoundError:
                open(f'{session_key}.sty', 'w').write(session_key)
                database = SQLiteSession(session_key)
                database.insert(self.phone, session_key, self.chat_id, self.api_client or Urls.get_url())

        if check_update:
            UpToDate(Version.__version__, 'https://raw.githubusercontent.com/Mester-Root/rubx/main/rb/version.sty').user
        
        if check_session:
            self.check_session: dict = __Top(self.session).detecting()
        
        if isinstance(base_logger, str):
            base_logger: str = logging.getLogger(base_logger)
        
        elif not isinstance(base_logger, logging.Logger):
            base_logger: str = base_log

        class Loggers(dict):
            def __missing__(self, key) -> ...:
                if key.startswith('rb.'):
                    key = key.split('.', maxsplit=1)[1]

                return base_logger.getChild(key)

        self._log = Loggers()
        # self.__name__ = base_logger
        
        Connection.timeout: int = timeout or 5
        clients.web.update({'lang_code': self.lang_code or 'en'}) # TODO: to set lang_code in rubx and android clients
        
        if not return_data_an_dict:
            Make.action: str = 'str'
        
        if headers:
            Connection.headers = headers
        if api_version:
            Connection.api_version = api_version
        if self.platform:
            Connection.platform = platform
        if city:
            Connection.city = city
        if proxy:
            Connection.proxy = proxy
        
    def __dir__(self):
        return dir(self)
    
    def __call__(self) -> (None):
        pass

    def __enter__(self):
        return (self)

    def __exit__(self, *args,
                 **kwargs) -> (None):
        pass

    @property
    def start(self): # TODO: set runner with start func
        pass
    
    @property
    def get_session(self) -> (str):
        return self.auth
    
    @property
    def get_storage(self) -> (str):
        return dumps({'session': SQLiteSession(self.auth).information()}, indent=2)

    @classmethod
    def run(cls, func: object,
            *args, **kwargs) -> None:
        
        '''
        running sync methods
        '''
        
        __import__('_thread').start_new_thread(func, *args, **kwargs)


Client = (RubikaClient)

class SetClient(
    RubikaClient,
    UserMethods,
    GroupMethods,
    ChannelMethods
    ):
    pass

class WebSocket(object):

    def __init__(self, session) -> (None):
        self.auth: str = session
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
            if mode == '1':
                self.__on_open(ws, '4')
            else:
                self.__on_send(ws)
        except Exception:
            pass
    
    @property
    def connection(self) -> (None):

        from websocket import create_connection

        ws, count = create_connection('wss://jsocket4.iranlms.ir:80'), 0
        self.__connector(ws)

        while 1:

            try:
                for (res) in [ws.recv()]:
                    
                    count: int = count.__add__(1)

                    if (count / 2)  == 30:
                        self.__connector(ws, '2')

                    elif (count / 2) == 50:
                        self.__connector(ws, '1')
                        count: int = 0

                    if len(str(res)) != 33:
                        yield self.__on_message(res)

            except Exception:
                pass

class EventBuilder(Client):
    
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

        '''
        # get all keys from a dictionary
        '''

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

    @property
    def action(self):
        return self.find_keys(keys=['author_type'])


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
    def find_rubika_channel_post(self):
        return findall(r'(rubika\.ir\/\w{4,25}\/\w{15})', self.raw_text)

    @property
    def find_rubika_private_link(self):
        return findall(r'(rubika\.ir\/join[c,g]\/\w{32})', self.raw_text)

    @property
    def find_chanel_private_link(self):
        return findall(r'(rubika\.ir\/joinc\/\w{32})', self.raw_text)

    @property
    def find_group_link(self):
        return findall(r'(rubika\.ir\/joing\/\w{32})', self.raw_text)

    @property
    def find_rubika_link(self):
        return findall(r'(rubika\.ir\/\w{4,25})', self.raw_text)

    @property
    def find_atsign(self):
        return findall(r'\@\w{4,25}', self.raw_text)

    @property
    def find_url(self):
        return findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})', self.raw_text)

    @property
    def is_rubika_channel_post(self):
        return bool(search(r'(rubika\.ir\/\w{4,25}\/\w{15})', self.raw_text))

    @property
    def is_rubika_private_link(self):
        return bool(search(r'(rubika\.ir\/join[c,g]\/\w{32})', self.raw_text))

    @property
    def is_chanel_private_link(self):
        return bool(search(r'(rubika\.ir\/joinc\/\w{32})', self.raw_text))

    @property
    def is_group_link(self):
        return bool(search(r'(rubika\.ir\/joing\/\w{32})', self.raw_text))

    @property
    def is_rubika_link(self):
        return bool(search(r'(rubika\.ir\/\w{4,25})', self.raw_text))

    @property
    def is_atsign(self):
        return bool(search(r'\@\w{4,25}', self.raw_text))

    @property
    def is_url(self):
        return bool(search(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})', self.raw_text))
    
    @property
    def is_admin(self):
        return any(user.get('member_guid') == self.author for user in SetClient(self.auth).get_group_admin_members(self.object_guid).get('data').get('in_chat_members'))
    
    @property
    def is_user(self):
        return self.action == 'User'
    
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
    def is_personal(self):
        return self.is_private
    
    @property
    def is_bot(self):
        return self.type == 'Bot'
    
    @property
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
    def author_object_guid(self):
        try:
            return self.author_object_guid

        except AttributeError:
            pass
    
    def guid_type(self, chat_id: str) -> str:
        if isinstance(chat_id, str):
            return Scanner.check_type(chat_id)
    
    def finder(self, filters) -> (object):
        
        if 'group_guid' in filters:
            return self.group_guid if not 'message' in self.original_update.keys() else self.message.group_guid
        elif 'channel_guid' in filters:
            return self.channel_guid if not 'message' in self.original_update.keys() else self.message.channel_guid
        elif 'user_guid' in filters:
            return self.user_guid if not 'message' in self.original_update.keys() else self.message.user_guid
        elif 'object_guid' in filters:
            return self.object_guid if not 'message' in self.original_update.keys() else self.message.object_guid
        else:
            return self.author_object_guid if not 'message' in self.original_update.keys() else self.message.author_object_guid
    
    def pin(self, chat_id: str = None,
            message_id: str = None) -> (dict):

        return SetClient(self.auth).set_pin_message(chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message_id = message or self.message_id, action='Pin')
    
    def unpin(self, chat_id: str = None,
              message_id: str = None) -> (dict):

        return SetClient(self.auth).set_pin_message(chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message_id = message or self.meesage_id, action='Unpin')

    def seen(self, chat_id: str = None,
             message: str = None) -> (dict):
        
        return SetClient(self.auth).seen_chats({chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']): message or self.message_id if not 'message' in self.original_update.keys() else self.message.message_id})
    
    def reply(self, *args, **kwargs) -> (dict):
        
        return SetClient(self.auth).send_message(*args, **kwargs)
    
    def respond(self, text: str, 
                action: str = 'author_object_guid') -> (dict):

        return SetClient(self.auth).send_message(text, self.finder(action), reply_to_message_id=self.message_id if not 'message' in self.original_update.keys() else self.message.message_id)
    
    def send(self, text,
             action: str = 'author_object_guid'):
        return SetClient.send_message(text, self.finder(action))
    
    def edit(self, text: str, chat_id: str = None,
             message_id: str = None, action: str = 'author_object_guid', *args, **kwargs) -> (dict):

        return SetClient(self.auth).edit_message(message_id = message_id or self.message_id, text=text, chat_id = chat_id or self.finder(action), *args, **kwargs)
    
    def forwards(self, to: str,
                 _from: str = None, messages: list = None) -> (dict):
        
        return SetClient(self.auth).forward_messages(_from or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), messages or [self.message_id], to)
    
    def download(self, chat_id: str = None,
                 message: str = None, name: str = None, *args, **kwargs) -> (dict):

        return SetClient(self.auth).get_file('message' if message else '', True, save_as=name, chat_id = chat_id or self.find_keys(keys=['object_guid', 'author_object_guid', 'channel_guid', 'group_guid', 'user_guid', 'bot_guid', 'service_guid']), message = message or self.find_keys(keys=['messaage_id']))

    def delete(self, chat_id: str = None,
               messages: list = None, action: str = None, *args, **kwargs) -> (dict):
        
        return SetClient(self.auth).delete_messages(messages or [self.message_id], chat_id or self.object_guid)

    def save(self, chat_id: str = None, 
            message_id: str = None, action: str = 'author_object_guid') -> (dict):

            return SetClient(self.auth).forward_messages(self.finder(action), [self.message_id], self.chat_id or self.user_guid)

    def activity(self, chat_id: str = None,
                 action: str = 'author_object_guid') -> (dict):
        return SetClient(self.auth).send_chat_activity(self.finder(action), 'is typing...')


class NewMessage(Client):
    
    def __init__(
        self,
        func        :   object,
        filters     :   list  =   None,
        pattern     :   str   =   None,
        commands    :   dict  =   None, 
        gets        :   tuple =   None,
        handle_name :   str   =   'handshake',
        *args
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


    def builder(self) -> iter:
        
        if not isinstance(self.filters, list):
            self.filters: list = [self.filters]
        
        for message in self.func(self.handle_name, get_messages=True, chat_ids=self.filters):
            
            if self.pattern:
                if not isinstance(self.pattern, str):
                    raise ValueError('oh pattern param is not string type.')
                if search(self.pattern, message.get('text') or message):
                    update = EventBuilder(message)
                    yield update

            elif self.commands:
                
                if not isinstance(self.commands, dict):
                    raise ValueError('oh commands param is not dictionary type.')
                    
                if any(cmd in message.get('text') for cmd in list(self.commands.keys())):
                    update = EventBuilder(message)
                    yield update

            elif self.gets:
                
                if not isinstance(self.gets, tuple) or isinstance(self.gets, list):
                    raise ValueError('oh gets param is not a tuple or list type.')
                
                if any(cmd in message for cmd in self.gets):
                    update = EventBuilder(message)
                    yield update

            else:
                update = EventBuilder(message)
                yield update

class Handler(Client):

    def __init__(self, starting: bool = True,
                 *args, **kwargs) -> (None):

        '''
        # Handler | Events


        ## Example:
            from rb import Handler, NewMessage

            with Handler(...) as client:
                client.on(NewMessage(client.handle, handle_name='ChatsUpdates').builder())
                def update(event):
                    pass

        ## Responses:
            - `HandShake`:

                message_updates:

                    {
                        'message_id': ...,
                        'message': {
                            'text': ...,
                            'message_id': ...,
                            'action': ...,
                            'type': ...,
                            'author_object_guid': ..., 
                            },
                        'user_guid': ...,
                        }

                chat_updates:
                    ...

                show_notifications:
                    ...

            - `ChatsUpdates`:
                {
                    'message_id': ...,
                    'text': ...,
                    'author_object_guid' ...,
                    'author_type': ... ,
                    'type': ...
                    }

            - `MessagesUpdates`:
                {
                    'message_id': ...,
                    'text': ...,
                    'author_object_guid' ...,
                    'author_type': ... ,
                    'type': ...
                    }
        '''
        
        super().__init__(starting, *args, **kwargs)
        self.starting = starting

    def __enter__(self):
        return self

    def __exit__(self, *args,
                 **kwargs) -> (None):
        pass

    def __appender(self, msg_id: str = None,
                    action: str = 'edit'):
        
        if action == 'edit':
            if not msg_id in open(self.auth+'-ids.sty', 'r').read():
                open(self.auth+'-ids.sty', 'a+').write(msg_id+'\n')
        else:
            open(self.auth+'-ids.sty', 'w')
    
    def handle(
            self,
            method              :   str                         =   'ChatsUpdates',
            get_chats           :   bool                        =   True,
            get_messages        :   bool                        =   True,
            chat_ids            :   str                         =   None,
            author_guid         :   str                         =   None,
            pattern             :   typing.Union[tuple, list]   =   None,
            show_notifications  :   bool                        =   False
            ) -> (dict):

        '''
        `method`: methods: `ChatsUpdates`, `MessagesUpdates`, `HandShake`
        `get_chats`: the chat updates
        `get_messages`: the message updates
        `chat_ids`: chat filter
        `author_guid`: author_filter
        `pattern`: the pattern is for get message filter: `('^\w{1}start', 'Hey! from rubx lib')`
        '''

        if not method or not isinstance(method, str) or not any(word in method.lower() for word in ('chatsupdates', 'messagesupdates', 'handshake', 'socket')):
            method: str = 'HandShake'

        if ('handshake' in method.lower() or 'socket' in method.lower()):

            for msg in self.hand_shake():

                if msg.get('type') == 'messenger':

                    res: dict = msg.get('data')

                    if get_chats and get_messages:
                        if not show_notifications:
                            res.pop('show_notifications')
                        yield res

                    elif get_messages:

                        for i in res.get('message_updates'):

                            if pattern:

                                if not isinstance(pattern, list) or isinstance(pattern, tuple):
                                    raise ValueError('pattern not a tuple or list type.')
        
                                if search(pattern[0], i.get('message').get('text') or ''):
                                    i.update({'pattern': pattern[1]})
                                    yield i
                            else:
                                yield i

                    elif get_chats:
                        for i in res.get('chat_updates'):
                            yield i

                    elif show_notifications:
                        for i in res.get('show_notifications'):
                            yield i

                    else:
                        res.update(res.get('message_updates'))
                        res.update(res.get('chat_updates'))
                        res.update(res.get('show_notifications'))
                        yield res

        elif ('chatsupdates' in method.lower()):

            while (1):
                
                try:
                    for msg in SetClient(self.auth).get_chats_updates().get('data').get('chats'):
                        
                        if not msg.get('last_message').get('message_id') in open(self.auth+'-ids.sty', 'r').read():
                            
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

            while (1):
                
                try:
                    if chat_ids:
                        
                        if not isinstance(chat_ids, list):
                            chat_ids: list = [chat_ids]
                            
                        for chat_id in chat_ids:
                            for msg in SetClient(self.auth).get_messages_updates(chat_id).get('data').get('updated_messages'):
                                if not msg.get('last_message').get('message_id') in open(self.auth+'-ids.sty', 'r').read().split('\n'):
                                    
                                    if pattern and isinstance(pattern, tuple) or isinstance(pattern, list):
                                        if search(pattern[0], msg.get('last_message').get('text')):
                                            yield [msg.get('last_message'), pattern[1]]
                                    else:
                                        yield msg.get('last_message')
                                
                                self.__appender(msg.get('last_message').get('message_id'), 'edit')
                except Exception:
                    ...

    def hand_shake(self) -> (dict):
        for message in WebSocket(self.auth).connection:
            yield message

    def handler(self, builder: object) -> (typing.Union[object,
                                                        iter, None]):
        
        '''
        ## EXAMPLE:
            
            from rb import Handler, EventBuilder, Filters

            client = Handler(...)
            
            # the funcs: `ChatsUpdates`, `MessagesUpdates`, `HandShake` # websocket
            
            client.add_event_handling(func='HandShake', events=dict(get_messages=True, get_chats=True))
            
            @client.handler
            def update(app: RubikaClient, message: EventBuilder, event):
                ...
        
        '''
        
        def decorator():

            methods = SetClient(self.auth)
            update = Handler(self.auth)
            
            if self.handling.get('events'):
                if not isinstance(self.handling['events'], dict):
                    self.handling.update({'events': dict(get_messages=True, get_chats=True)})
            else:
                self.handling.update({'events': dict(get_messages=True, get_chats=True)})
            if not self.handling.get('func') and isinstance(self.handling.get('func'), str) and self.handling.get('func').lower() in ['handshake', 'chatsupdates', 'messagesupdates']:
                self.handling.update({'func': 'chatsupdates'})
            
            for (event) in (update.handle(method=self.handling.get('func'), **self.handling.get('events') or {})):
                event.update({'auth': self.auth, 'chat_id': self.chat_id or ''})
                message = EventBuilder(event)
                builder(methods, message, event)
        
        self.__appender(action='create')
        
        while 1:
            try:
                decorator() # TODO: use the threading
            except Exception:
                pass
    
    def command_handler(self, func: object, *args): # to handling with custom func

        '''
        from rb import Handler, Filters, Performers

        client = Handler('session')

        def event(message):
            message.respond(message.pattern) # Filters.author - send message to user
        
        client.add_event_handling(Performers.chats_updates, event=dict(get_chats=True, get_messages=True, pattern=(client.regex('/start'), 'Hi from rubx lib.')))
        client.start = True
        client.command_handler(event)
        '''

        def updater(*args):

            @self.handler
            def update(app, message, event):
                func(message)
        if (self.starting):
            self.__appender(action='create')
            updater()

    def on(self, event) -> (typing.Union[object, None]):
        
        '''
        ## EXAMPLE:

            from rb import Handler, NewMessage
            
            client = Handler(...)
            
            @client.on(NewMessage(client.handle, handle_name='ChatsUpdates').builder())
            def update(event):
                ...
        
        '''
        
        def decorator(func) -> (None):
            return func

        return decorator

    def add_event_handling(self, **handlers) -> (None):
        # add a handler method and params
        self.handling.update({'func': handlers.get('func') or handlers.get('method'), 'events': handlers.get('events') or handlers.get('event')})
    
    def remove_event_handling(self, func: object):
        try:
            self.handling.pop(func)
        except KeyError:
            ...

    def regex(self, word: str) -> (compile):
        return compile(word)

# to finding all attr's
class Classer(object):

    @classmethod
    def create(cls, name, __base, authorise: list = [],
               exception: bool = True, *args, **kwargs) -> object:
        
        result = None
        if name in authorise:
            result = name

        else:
            attr = difflib.get_close_matches(name, authorise, n=1)
            
            if attr:
                return getattr(__base[0], attr[0])
            
            else:
                caller = inspect.getframeinfo(inspect.stack()[2][0])
                warn(
                    f'{caller.filename}:{caller.lineno}: do you mean'
                    f' "{name}", "{result}"? correct it')

        if result != None or not exception:
            if result == None:
                result = name
            # setattr(___base[0], result or name, lambda *args, **kwargs: ...)
            # return getattr(__base[0], name)
            return type(result, __base, {'__name__': result, **kwargs}) # add method to class

        raise AttributeError(f'module has no attribute ({name})')

# main class object to set all method for use.
class RubikaClient(SetClient): # TODO: add all methods
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __getattr__(self, name, *args, **kwargs) -> Classer:
        
        # `note`: for: if you forget the method name
        '''
        from rb import RubikaClient
        
        with RubikaClient('session') as client:
            print(client.getChatInfo(client, 'chat-guid')) # GetChatInfo, GETchatINFO, or ...
        '''

        # for: normally
        '''
        from rb import RubikaClient
        
        with RubikaClient('session') as client:
            print(client.get_chat_info('chat-guid'))
        '''
        
        method = Classer.create(name, (SetClient, ), dir(SetClient))
        
        try:
            return method(*args, **kwargs)
        except Exception:
            return method

# To use the async for methods
# TODO: set handler with async.
class Client(RubikaClient):
    
    def __init__(self, *args, **kwargs):

        '''
        from rb import Client

        async def run(*args):
            async with Client(...) as client:
                await client.start(client.send_message, 'Hey! from rubx', 'chat-guid')
        
        Client.run(run)
        '''

        super().__init__(*args, **kwargs)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs) -> (None):
        pass

    async def start(self, method: object, *args, **kwargs) -> (dict):
        '''
        get method func to async
        '''
        return method(*args, **kwargs)
    
    @staticmethod
    def run(func: object, *args) -> (None):
        '''
        run main func to use
        
        func | func()
        -------------
        '''
        try:
            __import__('asyncio').run(func())
        except Exception:
            __import__('asyncio').run(func)