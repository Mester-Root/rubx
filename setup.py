#!/bin/python

from setuptools import find_packages, setup

requires = ['requests', 'urllib3', 'datetime']
version = '10.2.8'

readme = '''
<p align="center">
    <a href="https://github.com/mester-root/rubx">
        <img src="https://raw.githubusercontent.com/Mester-Root/rubx/main/logo.png" alt="RUBX" width="128">
    </a>
    <br>
    <b>rubika client | python 3</b>
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
     •
</p>

# روبیکس | روبیکا
# Rubx | Rubika


## Messenger:

```python

from rb import StartClient 

with StartClient('session') as client:
   client.send_message('Hello from rubx', 'chat-guid')

```

### Or

```python
from rb import StartClient as Client

def respond(callable, params) -> dict:
    return callable(**params)

with Client(...) as client:
    print(
        respond(
            client.send_message,
            dict(chat_id=..., text='Hey')
            )
        )
```

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

@client.on(NewMessage(client.handle, handle_name=Performers.chats_updates))
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
client.start = True
client.command_handler(event)
```

## to using HandShake(WebSocket):

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

### docs coming soon ...

___________________________


## INSTALLING

![installed :) ](https://raw.githubusercontent.com/Mester-Root/rubx/main/2022-08-06%20(3).png)

```bash
pip install rubx
```


## UPGRADE
```
pip install rubx --upgrade
```

## CREATED BY:

    - saleh | rubika.ir/TheServer


# self rubika client with python3 RUBX module ![](https://i.imgur.com/fe85aVR.png)

## .. rubika library ..
_______________________

[![Python 3|2.7|3.x](https://img.shields.io/badge/python-3|3.0|3.x-yellow.svg)](https://www.python.org/)

[![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Mester-Root/rubx/main/LICENSE)

[![creator: ](https://img.shields.io/badge/Telegram-Channel-33A8E3)](https://t.me/rubx_library)

[![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/creator_ryson)
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

# view in github :
[![library](https://img.shields.io/puppetforge/mc/python?color=blue&label=RUBX&logo=RUBX&logoColor=red)](https://github.com/Mester-Root/rubx)

________________________

### the **special**:

- *[RUBX] > a library or module 'official' for rubika messnger with client server from iran ! for all .*
- *[RUBX] > full method and all methods rubika !*
- *[RUBX] > use api's rubika for you .*


نیاز مندد حمایت و استار های شما :), از صفحه گیت هاب این پروژه دیدن کنید و استار بدید.
-----
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
    python_requires="~=3.5",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires
)