<p align="center">
    <a href="https://github.com/mester-root/rubx">
        <img src="https://raw.githubusercontent.com/Mester-Root/rubx/main/icons/rubx-action.png" alt="Rubx" width="420">
    </a>
    <br>
    <b>Rubika Client API Framework for Python</b>
    <br>
    <a href="https://pypi.org/project/rubx">
        Homepage
    </a>
    •
    <a href="https://github.com/Mester-Root/rubx/tree/main/docs">
        Documentation
    </a>
    •
    <a href="https://github.com/Mester-Root/rubx/tree/main/Examples">
        Examples
    </a>
    •
    <a href="https://github.com/Mester-Root/rubx/tree/main/Tools">
        Tools
    </a>
</p>



Rubx | 🔶 | روبیکس
---------------------

## Messenger - مثال پیامرسان:

```python

from rb import RubikaClient # rb: is main package

with RubikaClient('session') as client:
   client.send_message('**Hey** __from__ ``rubx``', 'chat-guid')

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
            dict(chat_id=..., text='Hey')
            )
        )
```

### Or

## Shorcuts | مثالی از چند میانبر

```python
from rb import RubikaClient

with RubikaClient(...) as client:
    print(client == dict(text='Hey', chat_id='chat-guid')) # to send message
    # print(client * 'chat-guid') # to get chat info
   # use the operators
```

#### برای دیدن میانبر های کامل به مستندات ماژول مراجعه کنید.

### for: if you forget the method name
```python
from rb import RubikaClient

with RubikaClient('session') as client:
    print(client.getChatInfo(client, 'chat-guid')) # GetChatInfo, GETchatINFO, or ...
    # normally: client.get_chat_info('chat-guid')
```

## Rubino | مثال کلاینت روبینو

``` python

from rb import RubinoClient

with RubinoClient(__name__, 'session') as client:
    client.create_page(...)

```

## Handler | هندلر
#### Handler Examples

```python
from rb import Handler, EventBuilder, Filters, Performers

client = Handler(...)

# handlers: HandShake, ChatsUpdates, MessagesUpdates
client.add_event_handling(func=Performers.chats_updates, events=dict(get_chats=True, get_messages=True, pattern=('/start', 'Hey from rubx lib.')))

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

### Or

```python
from rb import Handler, Filters, Performers

client = Handler('session')

def event(message):
    message.respond(message.pattern, Filters.author)
        
client.add_event_handling(func=Performers.chats_updates, event=dict(get_chats=True, get_messages=True, pattern=('/start', 'Hi from rubx lib.')))
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


## Bot API Methods

### Example for api methods send message text
```python
from rb import BotAPI

with BotAPI(__name__, 'token') as app:
    app.send_message('chat-id', 'Hey!')
```

### Handler
```python
from rb import BotAPI

with BotAPI(__name__, 'token') as app:
    app.add_event_handling(('\w{1}start', 'Hello'))
    
    @app.handler
    def update(methods, update, event):
        ...
```


___________________________

## INSTALLING | نصب

```bash
pip install --user rubx
```

## UPGRADE | بروز رسانی

```
pip install rubx --upgrade
```


## CREATED BY:
    - saleh

_____________________________

Rubx - ⚡
========

  - Now the best ‍`sync‍` and `async` library for Rubika's was developed
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
   - The complete documentation and optimization.


# rubika client self with python3 | RUBX module ![](https://i.imgur.com/fe85aVR.png)


_______________________

[![Python 3|2.7|3.x](https://img.shields.io/badge/python-3|3.0|3.x-yellow.svg)](https://www.python.org/)   | [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Mester-Root/rubx/main/LICENSE)

[![creator: ](https://img.shields.io/badge/Telegram-Channel-33A8E3)](https://t.me/rubx_library) | [![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/ClientUser)

![issues](https://img.shields.io/github/issues/mester-root/rubx)      | ![forks](https://img.shields.io/github/forks/mester-root/rubx)

![stars](https://img.shields.io/github/stars/mester-root/rubx)   | ![license](https://img.shields.io/github/license/mester-root/rubx)

________________________


## **special**:
- *[RUBX] > a library 'official' for rubika messnger with client server.*
- *[RUBX] > full method .*


𝙍𝙪𝙗𝙭 𝙈𝙚𝙨𝙨𝙚𝙣𝙜𝙚𝙧
---------------
