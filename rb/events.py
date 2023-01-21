#!/bin/python

class Filters(str):
    group, channel, user, chat, author = 'group_guid', 'channel_guid', 'user_guid', 'object_guid', 'author_object_guid'

class Performers(str):
    chats_updates, messages_updates, hand_shake = 'ChatsUpdates', 'MessagesUpdates', 'HandShake'

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