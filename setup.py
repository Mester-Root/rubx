#!/bin/python

from setuptools import find_packages, setup

requires = ['requests', 'urllib3', 'datetime']
version = '10.4.8'

readme = '''
<p align="center">
    <a href="https://github.com/mester-root/rubx">
        <img src="https://raw.githubusercontent.com/Mester-Root/rubx/main/icons/rubx-action.png" alt="RuBx" width="420">
    </a>
    <br>
    <b>Rubika Client API Framework | Python 3</b>
    <br>
    <a href="https://github.com/Mester-Root/rubx/blob/main/README.md">
        Document
    </a>
     •
    <a href="https://t.me/rubx_library">
        Telegram
    </a>
     •
    <a href="https://rubika.ir/TheClient">
        Rubika
    </a>
</p>


# [Rubx] - rubika messenger

## Messenger:

```python

from rb import RubikaClient # rb: is main package

with RubikaClient('session') as client:
   client.send_message('Hello From Rubx', 'chat-guid')

```

### Or

```python
from rb import RubikaClient as Client

def respond(callable, params) -> dict:
    return callable(**params)

with Client(...) as client:
    print(
        respond(
            client.send_message,
            dict(
                chat_id=...,
                text='**Hey** @User@ R U __My__ ``Friend`` and ~~My Love~~'
                mention_user_ids=['u0...']),
            )
        )
    
    # print(respond(client.send_message, dict(chat_id=..., sticker=True, emoji_character='😜', sticker_id=..., )))
```

### Or

## shorcuts

```python
from rb import RubikaClient

with RubikaClient(...) as client:
    print(client == dict(text='Hey', chat_id='chat-guid')) # to send message
    # print(client * 'chat-guid') # to get chat info
    # use the operators

```

### for: if you forget the method name
```python
from rb import RubikaClient

with RubikaClient('session') as client:
    print(client.getChatInfo(client, 'chat-guid')) # GetChatInfo, GETchatINFO, or ...
    # normally: client.get_chat_info('chat-guid')
```

#### for show all operators and shortcuts go to docs


## Rubino

``` python

from rb import RubinoClient

with RubinoClient('session') as app:
    app.create_page(...)

```

## Handler
### Handler Examples

```python
from rb import Handler, EventBuilder, Filters

client = Handler(...)

# handlers: HandShake, ChatsUpdates, MessagesUpdates
client.add_event_handling(func='ChatsUpdates', events=dict(get_chats=True, get_messages=True, pattern=('/start', 'Hey from rubx lib.')))

@client.handler
def hello(app, message: EventBuilder, event):
    # to print message: print(message) or print(event)
    # to use all methods: app.create_objcet_voice_chat(...)
    message.respond(message.pattern, Filters.author) # filters: chat, group, channel, author
```

### Or

```python
from rb import Handler, NewMessage, Filters, EventBuilder, Performers

client = Handler(...)

@client.on(NewMessage(client.handle, handle_name=Performers.chats_updates).builder())
def update(event: EventBuilder):
    ... # event.respond('Hey', Filters.chat)

```

## Or

```python
from rb import Handler, Filters, Performers

client = Handler('session')

def event(message):
    message.respond(message.pattern, Filters.author)
        
client.add_event_handling(func=Performers.hand_shake, events=dict(get_chats=True, get_messages=True, pattern=('/start', 'Hi from rubx lib.')))
client.starting = True
client.command_handler(event)
```

## To using HandShake(WebSocket):

```python
from rb import Handler, EventBuilder, Filters, Performers

client = Handler('abc...', 'u0...')
client.add_event_handling(func=Performers.hand_shake, events=dict(get_messages=True, get_chats=False))
@client.handler
def update(app, update, event):
    if update.message.text == '/start':
        message.reply(text='Hello my dear', chat_id=update.message.author_object_guid, reply_to_message_id=update.message.message_id)
        # or using repond: message.respond('Hey!', Filters.author)
```

## Async methods

```python
from rb import Client # Client: asycn reader

async def run(*args):
    async with Client(...) as client:
        result = await client.start(client.send_message, 'Hey! from rubx', 'chat-guid')
        print(result)

Client.run(run)
```

### How to get keys from result?

```python
from rb import RubikaClient

with RubikaClient('session', return_data_an_dict=False) as client:
    print((client * 'chat-guid').data.chat) # get chat info: get data and get chat from a chat object
```

_____________________________

Rubx - ⚡
========

  - Now the best ‍`sync‍` and `asycn` library for Rubika's was developed
  - ⭐️ Thanks **everyone** who has starred the project, it means a lot!

**Rubx** is an sync **Python 3** rubika library to interact with Rubika's API
as a user or through a bot account (self API alternative).

    🔴 If you have code using Rubx before its 8.0.5 version, you must
    read docs to learn how to migrate. 💡

What is this?
-------------

🇮🇷 - Rubika is a popular messaging application. This library is meant
to make it easy for you to write Python programs that can interact
with Rubika. Think of it as a wrapper that has already done the
heavy job for you, so you can focus on developing an application.
This module provides all the desired methods with a very simple and beautiful user interface and has a very high speed.
Give your employer the best experience of a project.


Updating - 🌀 :
--------
    - Complete documentation and optimization.

___________________________


## INSTALLING
```bash
pip install rubx
```


## UPGRADE
```
pip install rubx --upgrade
```

## CREATED BY:

    - saleh


# self rubika client with python3 RUBX module ![](https://i.imgur.com/fe85aVR.png)

_______________________

[![Python 3|2.7|3.x](https://img.shields.io/badge/python-3|3.0|3.x-yellow.svg)](https://www.python.org/)

[![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Mester-Root/rubx/main/LICENSE)

[![Creator](https://img.shields.io/badge/Telegram-Channel-33A8E3)](https://t.me/rubx_library)

[![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/clientUser)
_______________________

<div align="center">

![issues](https://img.shields.io/github/issues/mester-root/rubx)
![forks](https://img.shields.io/github/forks/mester-root/rubx)
![version](https://img.shields.io/badge/version-v--1.0.1--beta-yellow)
![stars](https://img.shields.io/github/stars/mester-root/rubx)
![license](https://img.shields.io/github/license/mester-root/rubx)
![icon](https://raw.githubusercontent.com/Mester-Root/rubx/main/logo.png)
</div>


_______________________


### **special**:

- *[RUBX] > a library 'official' for rubika messnger with client server.*
- *[RUBX] > use api's rubika, and full methods.*

#### to use it, your python must support **type hint**.
'''

setup(
    name="rubx",
    version=version,
    description="Rubx Library For Rubika Iranina Messenger",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mester-root/rubx",
    download_url="https://github.com/mester-root/rubx/releases/latest",
    author="Saleh",
    author_email="m3st3r.r00t@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords=['messenger', 'python', 'self', 'rubx', 'rubix', 'rubikax', 'rubika', 'bot', 'robot', 'library', 'rubikalib', 'rubikalibrary', 'rubika.ir', 'web.rubika.ir', 'telegram'],
    project_urls={
        "Tracker": "https://github.com/mester-root/rubx/issues",
        "Channel": "https://t.me/rubx_library",
        "Source": "https://github.com/mester-root/rubx",
        "Documentation": "https://github.com/Mester-Root/rubx/blob/main/README.md",
    },
    python_requires="~=3.9",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires
)
