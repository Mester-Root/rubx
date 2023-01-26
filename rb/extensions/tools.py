#!/bin/python
# the tools version

class Clean(str):
    
    @staticmethod
    def html_cleaner(text: str) -> (str):
        return sub(compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), '', text)

class Scanner(object):
    
    @staticmethod
    def check_type(chat_id: str) -> (str):
             
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
                return {'key': cls.session, 'is_true': '', 'is_fake': exits, 'add': add, 'index_list': index}

        else:
            return {'key': cls.session, 'is_true': False, 'is_fake': True}

    def detecting(cls) -> (dict):
        return __Top(cls.session).__detecting()

class UpToDate(object):

    def __init__(self,
                 version: str, url: str) -> None:
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

        cls.image = image
        if isinstance(cls.image, str):
            cls.image = open(image, 'rb').read()

    @property
    def to_base64(cls) -> str:
        
        if cls.image:
            return base64.b64encode(cls.image).decode('utf-8')