#!/bin/python
# rubika clietn self channel methods

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
from .exceptions    import *
from .extensions    import *
from .sessions      import RubikaClient as Client
import typing


class ChannelMethods:


    __extend_class__ = 'ChannelMethods'


    def __enter__(self):
        return (self)

    def __exit__(self, *args,
                 **kwargs) -> None:
        pass


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


    set_channel_link        =   lambda self, chat_id: GetData.api(version=self.api_version or '5', method='setChannelLink', auth=self.auth, data={'channel_guid': self.__get_chat_id(chat_id)}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    check_channel_username  =   lambda self, username: GetData.api(version=self.api_version or '5', method='checkChannelUsername', auth=self.auth, data={'username': username}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)
    delete_channel          =   lambda self, chat_id: GetData.api(version=self.api_version or '5', method='removeChannel', auth=self.auth, data={'channel_guid': self.__get_chat_id(chat_id)}, mode=self.city, platform=self.platform or 'web', proxy=self.proxy)


    def add_channel_members(
        self        :   'Client',
        user_ids    :   (list),
        chat_id     :   (str)
        ) -> typing.Union[str, dict]:

            '''

            self.add_channel_members(['user guid', ]. chat_id='channel guid')
            
            PARAMETERS:
                1- user_ids a list user guids
                3- chat_id is channel guid
            '''
            
            chat_id, user_ids = self.__get_chat_id(chat_id), [self.__get_chat_id(ids) for ids in user_ids]

            return (GetData.api(version = self.api_version or '5', method = 'addChannelMembers', auth = self.auth,
                                data = {'channel_guid': chat_id, 'member_guids': user_ids}, mode = self.city,
                                platform = self.platform or 'web', proxy = self.proxy))


    def get_channel_all_members(
        self            :   ('Client'),
        chat_id         :   (str)   =   (None),
        search_text     :   (str)   =   (None),
        start_id        :   (str)   =   (None)
        ) -> typing.Union[str, dict]:
            
            '''
            self.get_channel_all_members(...)
            '''

            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    method      =   'getChannelAllMembers',
                    auth        =   self.auth,
                    data        =   {
                        'channel_guid'  :   self.__get_chat_id(chat_id),
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
        action  :   typing.Literal['Join', 'Leave'] = 'Join'
        ) -> typing.Union[str, dict]:

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
                        'channel_guid'   :   self.__get_chat_id(chat_id),
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
        ) -> typing.Union[str, dict]:
            
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
        ) -> typing.Union[str, dict]:

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
        ) -> typing.Union[str, dict]:
            
            '''
            `self.update_channel_username('channel-guid', 'username')`
            '''
            
            return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'updateChannelUsername',
                    data        =   {
                        'channel_guid'  :   self.__get_chat_id(chat_id),
                        'username'      :   username
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )


    def set_channel_admin(self: Client, chat_id: str,
                          member_guid: str, access_list: list = None,
                          action: str = 'SetAdmin') -> typing.Union[str, dict]:
        
        '''
        ## this method is for admin and unadmin a member chat
        
        
        USE:
            `self.set_channel_admin('group-guid', 'user-guid', [Accesses.admin.SendMessages])`
        
        PARAMS:
            1- `self` a is self object
            2- `chat_id` is group guid
            3- `member_guid` is a user guid
            4- `access_list` is for access user in group: from rub import accesses.admin or ["ChangeInfo", "ViewMembers", "ViewAdmins", "PinMessages", "SendMessages", "EditAllMessages", "DeleteGlobalAllMessages", "AddMember", "SetJoinLink"]
            5- `action` is action type: 'UnsetAdmin', 'SetAdmin'
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'setChannelAdmin',
                    data        =   {
                        'channel_guid'  :   self.__get_chat_id(chat_id),
                        'member_guid'   :   member_guid,
                        'action'        :   action,
                        'access_list'   :   access_list
                        },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )


    def channel_preview_by_join_link(self: Client, link: str) -> typing.Union[str, dict]:
        
        '''
        get channel info from link
        '''
        
        return (
                GetData.api(
                    version     =   self.api_version or '5',
                    auth        =   self.auth,
                    method      =   'channelPreviewByJoinLink',
                    data        =   {
                        'hash_link' :       findall(r'([A-Z0-9]+)$', link)[0]
                      },
                    mode        =   self.city,
                    platform    =   self.platform or 'web',
                    proxy       =   self.proxy
                )
            )


    def join_channel_by_link(self: Client, link: str) -> typing.Union[str, dict]:

        '''
        this method for join channel with link

        `self.join_channel_by_link('https://rubika.ir/joinc/...')`
        '''

        return (GetData.api(version = self.api_version or '4', auth = self.auth,
                            method = 'joinChannelByLink', data = {'hash_link': findall(r'([A-Z0-9]+)$', link)[0]}, mode = self.city,
                            platform = self.platform or 'android', proxy = self.proxy))


__all__ = ['ChannelMethods']