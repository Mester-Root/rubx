#!/bin/python
# the tools version

import re, json, base64


class Clean(str):

    @classmethod
    def html_cleaner(cls, text: str) -> (str):
        return re.sub(re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), '', text)


class Scanner(object):

    @classmethod
    def check_type(cls, chat_id: str) -> (str):
             
            if len(chat_id) > 2:

                if   (chat_id.lower().startswith('g0')):
                    return 'Group'

                elif (chat_id.lower().startswith('c0')):
                    return 'Channel'

                elif (chat_id.lower().startswith('u0')):
                    return 'User'

                elif (chat_id.lower().startswith('s0')):
                    return 'Service'

                elif (chat_id.lower().startswith('b0')):
                    return 'Bot'
                else                            :
                    raise ValueError(f'CHAT ID \'{chat_id}\' NOT FOUND.')
            else:
                raise ValueError(f'CHAT ID \'{chat_id}\' FALSE.')


class Maker(object):

    @classmethod
    def check_link(cls, link: str = None, client: object = None,
                   post: str = None, *args, **kwargs) -> (str):

        '''
        this is has a method for get link from a chat id
        
        `self.Make.check_link('https://rubika.ir/*', self)`
        '''

        if post and re.compile(r'rubika\.ir\/\S+').search(post):

            data = client.get_link_from_app_url(post)

            try:
                data = data.get('data').get('link').get('open_chat_data')
                return data.get('object_guid'), data.get('message_id')

            except Exception:

                try:
                    data = data.data.link.open_chat_data
                    return data.object_guid, data.message_id

                except Exception:
                    data = json.loads(list(client.last_response)[::-1].__iter__().__next__())['data']['link']['open_data_chat']
                    return data['object_guid'], data['message_id']


        if link.startswith('@') or not re.compile(r'rubika\.ir\/join[gc]\/\w+').search(link) and re.search(r'rubika\.ir/\w{4,25}', link):

            link: str = link.replace('https://', '').replace('rubika.ir/', '')
            result: dict = client.get_object_by_username(link.replace('@', ''))

            if not isinstance(result, dict):
                try:
                    result: dict = json.loads(result).get('data')
                except Exception:
                    result = json.loads(list(client.last_response)[::-1].__iter__().__next__())
                    result = result.get('data') or result
            else:
                result: dict = result.get('data') or result

            result: dict = result.get('user') or result.get('channel') or result.get('group')
            
            return result.get('user_guid') or result.get('channel_guid') or result.get('group_guid')


        elif len(link) == 56 or len(link) == 48 and 'joing' in link or 'joinc' in link:

            if 'joing' in link:

                result = client.group_preview_by_join_link(link)
                
                if not isinstance(result, dict):
                    try:
                        result = json.loads(result)
                        result = result.get('data') or result
                        return result['group']['group_guid']
                    
                    except Exception:
                        result = json.loads(list(client.last_response)[::-1].__iter__().__next__())
                        result = result.get('data') or result
                        return result['group']['group_guid']
                else:
                    result = result.get('data') or result
                    return result['group']['group_guid']

            elif 'joinc' in link:

                result = client.channel_preview_by_join_link(link)

                if not isinstance(result, dict):
                    try:
                        result = json.loads(result)
                        result = result.get('data') or result
                        return result['channel']['channel_guid']
                    
                    except Exception:
                        result = json.loads(list(client.last_response)[::-1].__iter__().__next__())
                        result = result.get('data') or result
                        return result['channel']['channel_guid']
                else:
                    result = result.get('data') or result
                    return result['channel']['channel_guid']


class Login(object):

    @classmethod
    def SignIn(cls, phone: str,
               UserMethods: object = None) -> (str):
        try:
            return UserMethods.sign_in(phone, UserMethods.send_code(phone, input('send type is SMS/Interval : '), password=input('please enter your password : ') if input('insert password y/n : ').lower() == 'y' else None).get('data').get('phone_code_hash'), input('please enter activation code : ')).get('data').get('auth') or '0'
        except Exception:
            from rb import RubikaClient
            return RubikaClient.sign_in(phone, RubikaClient.send_code(phone, input('send type is SMS/Interval : '), password=input('please enter your password : ') if input('insert password y/n : ').lower() == 'y' else None).get('data').get('phone_code_hash'), input('please enter activation code : ')).get('data').get('auth') or '0'


class _Top(object):

    @classmethod
    def __init__(cls, session: str) -> (None):

        '''
        detecting session key to chars echo
        '''

        cls.session = session

    @classmethod
    def __update(cls, key: str, check: bool,
                 is_fake: bool, adds: list, index_list: list) -> dict:
        return {'key': cls.session, 'check': None, 'is_fake': is_fake, 'adds': [*adds], 'index_list': index_list}

    
    @classmethod
    def detecting(cls) -> (dict):

        if isinstance(cls.session, str) and len(cls.session) == 32:
            exits, session, add, index = True, [*cls.session], '', []
            for key, n in zip(cls.session, range(len(cls.session))):
                
                if session.count(key) > 2:
                    exits: bool = True
                    cls.__update(**{'key': cls.session, 'check': None, 'is_fake': exits, 'adds': [*add], 'index_list': index})

                if session.count(key).__eq__(2):
                    add += key
                    index.extend([n])
                    exits: bool = False
            else:
                return cls.__update(**{'key': cls.session, 'check': None, 'is_fake': exits, 'adds': [*add], 'index_list': index})
        else:
            return {'key': cls.session, 'check': None, 'is_fake': True}


class UpToDate(object):

    def __init__(self,
                 version: str, url: str) -> None:

        '''
        upgrade module to last version from github repo
        '''

        self._ver, self._url = version, url

    @property
    def update(self) -> (str):

        if str(get(self._url).text) != self._ver:
            return 'notUpdated'
        else:
            return 'isUpdated'

    @property
    def user(self) -> (None):

        if self.update != 'isUpdated':
            if input('new version rubx now up to date? y/n : ').upper() == 'Y':
                
                os.system('pip install rubx --upgrade')
                
                if platform.system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')


class Thumbnail(object):

    @classmethod
    def __init__(cls, image: bytes) -> None:

        '''
        getting thumbnail from file bytes & make to base64
        '''

        cls.image = image
        if isinstance(cls.image, str):
            cls.image = open(image, 'rb').read()

    @property
    def to_base64(cls) -> str:

        if cls.image:
            return base64.b64encode(cls.image).decode('utf-8')