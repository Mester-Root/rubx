#!/bin/python
# rubika self client models

from pydantic import BaseModel
import typing


class File(BaseModel):
    file_id: str = None
    file_name: str = None
    dc_id: str = None
    access_hash_rec: str = None
    type: str = None
    time: str = None
    text: str = None
    is_edited: bool = None
    is_deleted: bool = None
    size: str = None


class Message(BaseModel):
    message_id: str = None
    text: str = None
    reply_to_message_id: str = None
    time: str = None
    is_edited: bool = None
    type: str = None
    author_type: str = None
    author_object_guid: str = None
    object_guid: str = None
    last_message_id: str = None
    group_guid: str = None
    channel_guid: str = None
    user_guid: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    member_guid: str = None
    file_inline: typing.Optional[File] = None
    count_seen: str = None


class Bot(BaseModel):
    original: str = None
    message: dict = None
    messages: list = None
    chats: list = None
    in_chat_members: list = None
    message_id: str = None
    text: str = None
    reply_to_message_id: str = None
    time: str = None
    is_edited: bool = None
    type: str = None
    author_type: str = None
    author_object_guid: str = None
    object_guid: str = None
    last_message: typing.Optional[Message] = None
    abs_object: typing.Optional[Message] = None
    count_seen: str = None
    group_guid: str = None
    channel_guid: str = None
    user_guid: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    title: str  = None
    description: str = None
    file_inline: typing.Optional[File] = None
    last_message_id: str = None
    next_start_id: str = None


class Result(BaseModel):
    status: str = None
    status_det: str = None
    data: typing.Optional[Bot] = None


class Attrs(object):

    @classmethod
    def create(cls, __names: dict, __bases: tuple = (Bot, ), /,
               action: str = 'bot', *args, **kwargs) -> typing.Union[Bot, Message, File, Result, object]:
        
        
        '''
        data = {'chat_id': ..., 'message_id': ...}
        
        print(Attr.create(data))
        '''

        __names.update({'original': 'updates'})
        
        for name in __names.keys():
            setattr(Bot, name, __names.get(name))
            #type(name, (Bot, ), {'__name__': name, name: __names.get(name)})

        for attr, name in zip(__names.keys(), map(lambda name: getattr(Bot, name), __names.keys())):
            if not name:
                delattr(Bot, attr)

        return Message(**__names) if action.__eq__('message') else Bot(**__names) if action.__eq__('bot') else File(**__names) if action.__eq__('file') else Result(**__names)


__all__ = ['Attrs']