#!/bin/python

from requests       import get
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
import typing

Client = 'RubikaClient'

class GroupMethods:

    def __enter__(self):
        return (self)

    def __exit__(
        self,
        *args,
        **kwargs
        ) -> (None):
        pass

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
                - `action`: is a action type. actions: 'SetAdmin', UnsetAdmin''
            '''

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