#!/bin/python

import pydantic, typing

'''
from rb.responses import Self
from rb import RubikaClient

with RubikaClient(...) as client:
    print(client == Self.Text(chat_id=..., text='Hello'))
'''

# Self Message Text Parser
class Self(object):
    
    '''
    from rb.responses.Self import *
    '''
    
    class Text(pydantic.BaseModel):
        chat_id: str
        text: str
        reply_to_message_id: str

    class Forward(pydantic.BaseModel):
        from_object_guid: str
        message_ids: typing.Optional[list]
        to_object_guid: str

    class Delete(pydantic.BaseModel):
        chat_id: str
        message_ids: typing.Optional[list]
    
    class Edit(pydantic.BaseModel):
        chat_id: str
        new_text: str

    __all__ = ['Text', 'Forward',
               'Delete', 'Edit']

'''
from rb import RubikaClient
from rb.responses.Bot import Text

with RubikaClient(...) as client:
    print(`client == Text(chat_id=..., text=...))`
'''

# Bot Message Text Parser
class Bot(object):
    
    '''
    from rb.responses.Bot import *
    '''
    
    class Text(pydantic.BaseModel):
        chat_id: str
        text: str

    class Forward(pydantic.BaseModel):
        from_chat_id: str
        message_id: typing.Optional[str]
        to_chat_guid: str

    class Delete(pydantic.BaseModel):
        chat_id: str
        message_id: typing.Optional[str]
    
    class Edit(pydantic.BaseModel):
        chat_id: str
        text: str
        message_id: str

    __all__ = ['Text', 'Forward',
               'Delete', 'Edit']

# TODO: add all methods