#!/bin/python

import warnings, sys, os, inspect, typing
from requests       import get
from pathlib        import Path
from random         import choice, randint, sample
from re             import findall, search, sub, compile, escape
from time           import sleep, gmtime, localtime
from datetime       import datetime
from json           import load, loads, dumps
from .crypto        import Encryption
from .connection    import GetData, Urls
from .clients       import *
from .exceptions    import *
from .extensions    import *
from .parser        import (MessageEmpty, MessageEntityBold,
                            MessageEntityCode, MessageEntityItalic,
                            MessageEntityHashtag, MessageEntityMention,
                            MessageEntityMentionName, MessageEntityPre,
                            MessageEntityStrike, MessageEntityTextUrl,
                            MessageEntityUnderline, MessageEntityUnknown,
                            MessageEntityUrl, Metas, Tags, MetaDataLoader)

Client = 'RubikaClient'

class UserMethods:
    
    # to use the `with`
    def __enter__(self: Client):
        return (self)

    def __exit__(
        self: Client, *args,
        **kwargs) -> (None):
        pass
    
    # new shortcut to use the first important methods
    # to usage of operators
    
    def __eq__(self, kwargs) -> (dict):
        
        
        # Example:
        '''
        from rb import RubikaClient
        
        with RubikaClient(...) as client:
            print(client == dict(chat_id=..., text=...)) # to send_message
        
        shortcut:
            self == dict(chat_id=..., text=...)
        '''
        
        return self.send_message(**kwargs)
    
    def __ge__(self, kwargs) -> dict:
        
        '''
        self >= dict(chat_id=..., text=...)
        '''
        
        return self.edit_message(**kwargs)
    
    def __gt__(self, *args, **kwargs):
        
        '''
        self > 'chat-guid'
        '''
        
        return self.get_chat_last_message(*args, **kwargs)
    
    def __ne__(self, kwargs) -> dict:
        
        '''
        self != dict(message_ids=[...,], chat_id=...)
        '''
        
        return self.delete_messages(**kwargs)
    
    def __lt__(self, kwargs) -> dict:
        
        '''
        self < dict(message_id=..., chat_id=...)
        '''
        
        return self.set_pin_message(**kwargs)
    
    def __le__(self, *args) -> dict:
        
        '''
        self <= {'chat':'message'}
        '''
        
        return self.seen_chats(*args)
    
    def __add__(self, kwargs) -> dict:
        
        '''
        self + dict(from_object=..., message_ids=[], to=...)
        '''
        
        return self.forward_messages(**kwargs)
    
    def __sub__(self, kwargs) -> dict:
        
        '''
        self - dict(message={})
        '''
        
        return self.get_file(**kwargs)
    
    def __mul__(self, *args) -> dict:
        
        '''
        self * 'chat-guid'
        '''
        
        return self.get_chat_info(*args)
    
    def __floordiv__(self, kwargs) -> dict:
        
        '''
        self // dict(...)
        '''
        
        return self.send_movie(**kwargs)
    
    def __truediv__(self, kwargs) -> dict:
        
        '''
        self / dict(...)
        '''
        
        return self.send_music(**kwargs)
    
    def __mod__(self, kwargs) -> dict:
        
        '''
        self % dict(...)
        '''
        
        return self.send_voice(**kwargs)
    
    def __pow__(self, kwargs) -> dict:
        
        '''
        self ** dict(...)
        '''
        
        return self.send_document(**kwargs)

    def __lshift__(self, kwargs) -> dict:
        
        '''
        self << dict(...)
        '''
        
        return self.send_location(**kwargs)
    
    def __rshift__(self, kwargs) -> dict:
        '''
        self >> dict(chat_id=..., action='Block')
        '''
        return self.set_block_user(**kwargs)
    
    def __and__(self, *args) -> dict:
        
        '''
        self & dict(...)
        '''
        
        return self.get_chat_last_message_id(*args)
    
    def __or__(self, *args) -> dict:
    
        '''
        self | dict(...)
        '''
        
        return self.get_chat_last_text(*args)

    def __xor__(self, *args) -> dict:
    
        '''
        self ^ 'chat-guid'
        '''
        
        return self.get_chat_last_object(*args)
    
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
        ) -> (dict):

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
        ) -> (dict):

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
        mode    : (str),
        text    : (str),
        user_ids: list = None
        ) -> (list):

        '''
        mode: to use a action type: html, markdown

        markdown [text]:

            **: Bold Type
            __: Italic Type
            ~~: Strike Type
            ``: Mono Type
            ```: Mono Type For Code
            @: To Mention Text

            Excample: '**Hey** ! @My Friend@ __i love__ ``you`` \n ```codes```'
        
        user_ids: to use the mention: '@You@ and @you@', ['u0...', 'u0...']
        '''

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
            [results.append({'from_index': mIndex, 'length': len(mWord), 'type': 'Mono'}) for mIndex, mWord in zip(mResult, monos)]

            return results, realText

        elif (mode.lower().startswith('markdown')):
            return Metas(text, user_ids=user_ids).checker
    
    @property
    def checkAuth(self) -> (dict):

        '''
        this method for checking your auth ke
        '''

        if (not 'NOT_REGISTERED' in list((etData.api(version='4', auth=self.auth, method='', data={}, mode=self.city, proxy=self.proxy, platform='android')).keys())):
            
            return {'session': 'ok'}
        else:
            return {'session'    :   'error'}

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
            frequest, bytef = self.request_send_file(file), open(file, 'rb+').read()
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
        
        # TODO: use the tinytag module
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
    def get_image_size(image_bytes: bytes) -> (list):
        
        from io import BytesIO
        from PIL.Image import open as openF
        
        im = openF(BytesIO(image_bytes))
        (width, height) = (im.size)
        
        return [width, height]

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
        parse_mode          :   (str)   =   None,
        mention_user_ids    :   (list)  =   None
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
            
            if parse_mode or '__' in text or '**' in text or '``' in text or '```' in text or mention_user_ids or len(findall(r'<(.*?)>', text)) + 1 >= 2:
                
                parse_mode: str = parse_mode or ''
                
                if parse_mode.lower() == 'markdown' or mention_user_ids or any([*text].count(meta) >= 4 for meta in ('_', '*', '`')):
                    
                    find: bool = True
                    
                    if search(r'(\@.*?\_\_.*?\_\_\w+)|(\@.*?\_\_\w+\_\_\w+)|(\@.*?\_\_\_\_\w+)', text):
                        if mention_user_ids or '__' in sub(compile(r'(\@.*?\_\_.*?\_\_\w+)'), '', text) or '**' in text or '``' in text:
                            pass # TODO: set a func to use
                        else:
                            find: bool = False

                    if find:
                        base: list = UserMethods.parsation('markdown', text, user_ids=mention_user_ids)
                        data.update({'metadata': {'meta_data_parts': base[0]}, 'text': base[1]})

                elif parse_mode.lower() == 'html' or search(r'<(.*?)>', text):
                    base: list = UserMethods.parsation(parse_mode or 'HTML', text)
                    data.update({'metadata': {'meta_data_parts': base[0]}, 'text': base[1]})

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
        self                :   ('Client'),
        message_id          :   (str),
        new_text            :   (str),
        chat_id             :   (str)   =   (None),
        username            :   (str)   =   (None),
        link                :   (str)   =   (None),
        metadata            :   (list)  =   (None),
        mention_user_ids    :   (list)  =   (None)
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

        if (parse_mode or mention_user_ids or text.startswith('__') or text.startswith('**') or text.startswith('``') or len(findall(r'<(.*?)>', text)) + 1 >= 2):
                
                parse_mode: str = parse_mode or ''
                
                if parse_mode.lower() == 'markdown' or mention_user_ids or any([*text].count(meta) >= 4 for meta in ('_', '*', '`')):
                    
                    find: bool = True
                    
                    if search(r'(\@.*?\_\_.*?\_\_\w+)|(\@.*?\_\_\w+\_\_\w+)|(\@.*?\_\_\_\_\w+)', text):
                        if '__' in sub(compile(r'(\@.*?\_\_.*?\_\_\w+)'), '', text) or '**' in text or '``' in text:
                            pass # TODO: set a func to use
                        else:
                            find: bool = False

                    if find:
                        base: list = UserMethods.parsation(parse_mode or 'markdown', text, user_ids=mention_user_ids)
                        data.update({'metadata': {'meta_data_parts': base[0]}, 'text': base[1]})

                elif parse_mode.lower() == 'html' or search(r'<(.*?)>', text):
                    base: list = UserMethods.parsation(parse_mode or 'HTML', text)
                    data.update({'metadata': {'meta_data_parts': base[0]}, 'text': base[1]})

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
        thumbnail           :   (str)   =   ('.'),
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
    
            uresponse: (list) = self.upload_file(file)
            
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
            
            uresponse: list = self.upload_file(file)
            
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
            
            uresponse: list = self.upload_file(file)
            
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
                            'thumb_inline'      :   thumbnail or Thumbnail(open(file, 'rb+'), width, height).to_base64,
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
                
                message: dict = kwargs.get('message')

                if not isinstance(message, dict):
                    message: dict = self.get_messages_by_id(kwargs.get('chat_id'), [str(message)])['data']['messages'][0]

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

                open(kwargs.get('save_as') or kwargs.get('saveAs') or f'{file_name}', 'wb+').write(result)

                return {
                    'status'    :   'saved',
                    'file_name' :   kwargs.get('save_as') or kwargs.get('saveAs') or file_name
                    }

            else:
                return result

    def download(self, *args, **kwargs) -> typing.Union[dict, str]:
        return self.get_file(*args, **kwargs)
    
    def method(name: str, types: str, file: str, *args, **data) -> dict or ...:
        
        import os
        methods: dict = __import__('json').load(open(os.path.join(os.path.dirname(os.getcwd()), file)))
        
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
        ) -> (dict):
            
            '''
            self.send_chat_activity('chat-guid', 'is typing...')
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
        ) -> (dict):
            
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
        ) -> (dict):
            
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
        ) -> (dict):
            
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
        ) -> (dict):
            
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
        ) -> (dict):
            
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
        ) -> (dict):
            
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
        ) -> (dict):
        
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
        self                :   Client,
        chat_id             :   str,
        user_guids          :   list,
        text                :   str,
        reply_to_message_id :   str   =   None
        ) -> (dict):

        '''
        self.mention_text('chat-guid', ['u0...'], '@hi@...')
        '''

        mention: tuple = Tags(text).checker(user_guids)

        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'sendMessage',
                    data        =   {'object_guid': chat_id, 'rnd': str(randint(100000,999999999)), 'reply_to_message_id': reply_to_message_id}.update({'text': mention[1], 'metadata': {'meta_data_parts': mention[0]}}),
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )

    def add_folder(self: Client, name: str, **kwargs) -> (dict):
        
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
        chat_id     :   str,
        text        :   str,
        button_id   :   str,
        message_id  :   str
        ) -> (dict):
            
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

    def send_report(
        self        :   Client,
        report_text :   str
        ) -> (dict):

        '''
        this method for send report to @supportbot
        '''

        def event():
            
            self.send_message(text='/start', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7')
            sleep(0.5)
            self.send_message(text='سؤال دارم', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='question')
            sleep(0.5)
            get: list = self.get_messages_interval(chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', middle_message_id=self.get_chat_last_message_id('b0Y0a2cafbaf668e282d2dc02a1fe2a7'))['data']['messages']
            self.send_messag_api_call(text='گزارش محتوای خلاف قوانین', chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='faq_5f0069d7108cd24b2a958dad', message_id=str(get[int(len(get)-1)]['message_id']))
            sleep(0.5)
            get: list = self.get_messages_interval(chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', middle_message_id=self.get_chat_last_message_id('b0Y0a2cafbaf668e282d2dc02a1fe2a7'))['data']['messages']
            self.send_messag_api_call(text=report_text, chat_id='b0Y0a2cafbaf668e282d2dc02a1fe2a7', button_id='newtextq_5f0069d7108cd24b2a958dad', message_id=str(get[int(len(get)-1)]['message_id']))
            
            return {'status': 'sended',
                    'report_text': report_text}

        return event()

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
        thumbnail           :   str                     =   None,
        parse_mode          :   str                     =   None
        ) -> (dict):
        
        '''
        `self.send_movie('chat-guid', 'vid.mp4')`
        '''

        uresponse: list = self.upload_file(file)

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
                'thumb_inline'      :   thumbnail or Thumbnail(open(file, 'rb+').read(), width, height).to_base64,
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
    
    def send_video(self, *args, **kwargs) -> dict:
        return self.send_movie(*args, **kwargs)
    
    def send_film(self, *args, **kwargs) -> dict:
        return self.send_movie(*args, **kwargs)

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
        uresponse: list = self.upload_file(file)
        
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

    def send_sound(self, *args, **kwargs):
        return self.send_music(*args, **kwargs)
    
    def get_chat_last_message_id(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_message_id('chat-guid') # the res is last message id from a chat: '99999...'`
        '''
        
        result = self.get_chat_info(chat_id)
        if isinstance(result, dict):
            result: str = result.get('data').get('chat').get('last_message_id')
        else:
            result: str = result.data.chat.last_message_id
            
        return result

    def get_chat_last_text(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_text('chat-guid') # the res is last text from a chat`
        '''
        
        result = self.get_chat_info(chat_id)
        
        if isinstance(result, dict):
            result: str = result.get('data').get('chat').get('last_message').get('text')

        else:
            resutl: str = result.data.chat.last_message.text
        
        return result
        
    def get_chat_last_object(self, chat_id: str) -> (str):
        
        '''
        `self.get_chat_last_object('chat-guid') # the res is a chat guid`
        '''
        
        result = self.get_chat_info(chat_id)
        
        if isinstance(result, dict):
            result: str = result.get('data').get('chat').get('last_message').get('object_guid')

        else:
            result: str = result.data.chat.last_message.object_guid
        
        return result
        
    def get_chat_first_message(self, chat_id: str) -> (dict):
        
        '''
        # TO GET FIRST MESSAGE A CHAT 
        
        `self.get_first_message('chat-guid') # the res: {'object_guid': ..., 'text': ..., 'message_id': ...,}`
        '''
        
        data: dict = self.get_messages_interval(chat_id=chat_id, middle_message_id=0)
        
        if isinstance(data, dict):
            data: list = data.get('data').get('messages')
        else:
            data: list = data.data.messages

        if len(data) < 1:
            return (self.get_messages_interval(chat_id=chat_id, middle_message_id='1').get('data').get('messages')[0])
        else:
            return (data[0])

    def get_last_message(self, chat_id: str) -> (dict):
        
        '''
        `self.get_last_message('chat-guid') # the res is a dictionary from a chat: {'object_guid', ..., 'text': ..., 'message_id': ..., }`
        '''
        
        result = self.get_chat_info(chat_id)
        
        if isinstance(result, dict):
            maked: dict = result.get('data').get('chat').get('last_message')
        else:
            maked: dict = result.data.chat.last_message
        
        return maked 

    def get_last_message_id(self, chat_id: str) -> str:
        return self.get_chat_last_message_id(chat_id)

    def chat_possession_transition(self, *args) -> (dict):
        pass
