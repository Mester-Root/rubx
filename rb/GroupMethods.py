#!/bin/python
# rubika client group self methods

from requests       import get, post
from pathlib        import Path
from random         import choice, randint, sample
from re             import findall, search, sub, compile, escape
from time           import sleep, gmtime, localtime
from datetime       import datetime
from json           import load, loads, dumps
from .crypto        import Encryption
from .connection    import GetData, Urls
from .UserMethods   import UserMethods
from .clients       import *
from .exceptions        import *
from .extensions    import *
from .sessions      import RubikaClient as Client
import typing


class GroupMethods:


    __extend_class__ = 'GroupMethods'


    def __enter__(self):
        return (self)

    def __exit__(
        self, *args,
            **kwargs) -> (None):
        pass


    get_display_as_in_group_voice_chat = lambda self, chat_id: GetData.api(version=self.api_version or '5', method='getDisplayAsInGroupVoiceChat', auth=self.auth, data={'chat_guid': chat_id}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)


    def __link_scanner(self, link: str) -> str:
        
        '''
        this is has a method for check hash link from a private link
        '''

        if not link.__contains__('/') and not search(r'[A-Z0-9]+', link):
            if len(link).__lt__(32):
                raise ValueError('\'link\' parameter is invalid')
            else:
                return findall(r'([A-Z0-9]+)$', link.upper())[0]

        else:
            return findall(r'([A-Z0-9]+)$', link)[0]


    def __get_chat_id(self, chat_id: str) -> str:
        '''
        `self.__get_chat_id('@username')`
        '''

        if chat_id.__eq__('me'):
            chat_id: str = self.username or self.chat_id

        if not compile(r'^g0\w+$|^u0\w+$|^s0\w+$|^c0\w+$|^b0\w+$|rubika\.ir\/\w+|\@\w+').search(chat_id):
            chat_id: str = '@' + chat_id

        if compile(r'rubika\.ir\/\w+|\@\w+').search(chat_id):
            chat_id: str = Maker.check_link(link=chat_id, client=self)

        return chat_id


    def ban_group_member(
        self            :   ('Client'),
        user_id         :   (str)   =   (None),
        chat_id         :   (str)   =   (None),
        action          :   (str)   =   ('Set'),
        ) -> typing.Union[str, dict]:

        '''
        `self.ban_group_member(user_id='chat id or guid', chat_id='chat guid')`
        
        PARAMETRS:
            1- self - self object
            2- user_id - target guid or chat id, username or link
            3- chat_id or username, link
            4- action is actions type: 'Set', 'Unset'
        '''

        chat_id, user_id = self.__get_chat_id(chat_id), self.__get_chat_id(user_id)

        return (
            GetData.api(version = self.api_version or '4',
                        method = 'banGroupMember', auth = self.auth,
                        data = {'group_guid': chat_id, 'member_guid': user_id, 'action': action}, proxy = self.proxy,
                        mode = self.city, platform = self.platform or 'android',))


    def add_group_members(
        self        :   'Client',
        chat_id     :   (str)   =   (None),
        user_ids    :   (list)  =  (None),
        *args,
        **kwargs,
        ) -> typing.Union[str, dict]:
            
            '''
            self.add_group_members(['user-guid', ], chat_id='group-guid')
            
            ## PARAMETERS:
                1- `self object`
                2- `chat_id is group guid`
                3- `user_ids is targets guid`
                
               
            '''
            
            chat_id, user_ids = self.__get_chat_id(chat_id), [self.__get_chat_id(user_id) for user_id in user_ids]
            
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
        ) -> typing.Union[str, dict]:

            '''
            self.get_group_admin_members('chat guid')
            
            PARAMETERS:
                -1 self is a self object
                -2 chat_id is chat guid, username or link
            '''

            chat_id: str = self.__get_chat_id(chat_id)

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
        ) -> typing.Union[str, dict]:
            
            
            '''
            from rubx import accesses
            self.set_group_default_access([accesses.SendMessages, ...], 'chat guid')
            
            PARAMETERS:
                1- self is a self object
                2- access_list is a list for users access
                3- chat_id is chat guid, username or link
            '''

            chat_id: str = self.__get_chat_id(chat_id)
            
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
        ) -> typing.Union[str, dict]:
            
            '''
            self.get_group_all_members('chat guid')
            
            PARAMETERS:
                1- chat_id is chat guid (group type), username or link
                2- start_id is for geting next member. and to get start_id: get key 'next_start_id'
                - END
            '''

            chat_id: str = self.__get_chat_id(chat_id)

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


    def get_group_link(
        self    :   ('Client'),
        chat_id :   (str)
        ) -> typing.Union[str, dict]:
            
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
        ) -> typing.Union[str, dict]:
            
            '''
            `self.get_group_link('group-guid')`
            note: this method for admin group
            
            PARAMETERS:
                1- self is a self object
                2- chat_id is group guid or old link
                - END
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        ) -> typing.Union[str, dict]:
            
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
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        action          :   (str)   =   ('SetAdmin')
        ) -> typing.Union[str, dict]:

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
                - `action`: is a action type. actions: 'SetAdmin', UnsetAdmin''
            '''
            
            chat_id, user_id = self.__get_chat_id(chat_id), self.__get_chat_id(user_id)
            
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
        ) -> typing.Union[str, dict]:
            
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
                        'hash_link'   :   self.__link_scanner(link)
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )


    def group_preview_by_join_link(
        self    :   ('Client'),
        link    :   (str)
        ) -> typing.Union[str, dict]:

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
                        'hash_link'   :   self.__link_scanner(link)
                        },
                    mode        =   self.city,
                    proxy       =   self.proxy,
                    platform    =   self.platform or 'web'
                )
            )


    def leave_group(
        self    :   ('Client'),
        chat_id :   (str)
        ) -> typing.Union[str, dict]:
            
            '''
            this method for leave the group
            
            USE:
                self.leave_group('group guid') # g0...
            PARAMETERS:
                1- self is a self object
                2- chat_id is group guid or link
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        ) -> typing.Union[str, dict]:

            '''
            self.start_voice_chat('chat-guid')
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        ) -> typing.Union[str, dict]:
            
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
        ) -> typing.Union[str, dict]:
            
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
        action  :   typing.Literal['Mute', 'Unmute', 'Pin', 'Unpin']
        ) -> typing.Union[str, dict]:

            '''
            USE:
                self.set_action_chat('chat-guid', 'Pin')
            PARAMS:
                1- self is a self object
                2- chat_id is chat guid
                3- action is a action type. actions: 'Mute', 'Unmute' | 'Pin', 'Unpin'
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        sdp_offer_data  :   str) -> typing.Union[str, dict]:

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


    def leave_group_voice_chat(
        self            :   Client,
        chat_id         :   str,
        voice_chat_id   :   str
        ) -> typing.Union[str, dict]:
            
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
        ) -> typing.Union[str, dict]:
            
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
        title                       :   str = None,
        description                 :   str = None,
        chat_history_for_new_members:   typing.Literal[None, 'Hidden', 'Visible'] = None
        ) -> typing.Union[str, dict]:
            
            '''
            self.edit_group_info('chat-guid', 'name', 'bio')
            
            actions: Hidden, Visible
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'editGroupInfo',
                    data        =   {
                        'group_guid'        :   chat_id,
                        'title'             :   title,
                        'description'       :   description,
                        'updated_parameters':   ['title' if title else None, 'description' if title else None, 'chat_history_for_new_members' if chat_history_for_new_members else None]
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
        ) -> typing.Union[str, dict]:
            
            '''
            self.get_banned_group_members('chat-guid') # get 'next_start_id' from respone to star_id param
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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
        ) -> typing.Union[str, dict]:
            
            '''
            self.get_group_mention_list('chat-guid')
            '''
            
            chat_id: str = self.__get_chat_id(chat_id)
            
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


    def delete_no_access_group_chat(self: Clean, chat_id: str) -> typing.Union[str, dict]:
        
        '''
        self.delete_no_access_group_chat('group-guid')
        '''
        
        chat_id: str = self.__get_chat_id(chat_id)
        
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


    def get_common_groups(self, user_id: str) -> typing.Union[str, dict]:
        '''
        `self.get_common_groups('u0...')`
        '''
        
        user_id: str = self.__get_chat_id(user_id)
        
        return (GetData.api(version = self.api_version or '4', auth = self.auth,
                            method = 'getCommonGroups', data = {'user_guid': user_id},
                            mode = self.city, platform = self.platform or 'android',
                            proxy = self.proxy))


    def get_group_online_count(self, chat_id: str) -> typing.Union[str, dict]:
        '''
        `self.get_group_online_count('g0...')`
        '''
        
        chat_id: str = self.__get_chat_id(chat_id)
        
        return (GetData.api(version = self.api_version or '4', auth = self.auth,
                            method = 'getGroupOnlineCount', data = {'group_guid': chat_id},
                            mode = self.city, platform = self.platform or 'android',
                            proxy = self.proxy))


__all__ = ['GroupMethods']