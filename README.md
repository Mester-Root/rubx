![Rubika](https://raw.githubusercontent.com/Mester-Root/rubx/main/logo.png)


# Rubx | 🔶
### Rubika


## Messenger:

```python

from rb import StartClient 

with StartClient('session') as client:
   client.send_message('Hey from rubx', 'chat-guid')

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

with RubinoClient('session') as client:
    client.create_page(...)

```

## Handler
#### Handler Examples

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
from rb import Handler, NewMessage, Filters, EventBuilder

client = Handler(...)

@client.on(NewMessage(client.handle, handle_name='ChatsUpdates'))
def update(event: EventBuilder):
    ... # event.respond('Hey', Filters.chat)

```

### Or

```python
from rb import Handler, Filters

client = Handler('session')

def event(message):
    message.respond(message.pattern, Filters.author)
        
client.add_event_handling('ChatsUpdates', event=dict(get_chats=True, get_messages=True, pattern=('/start', 'Hi from rubx lib.')))
client.start = True
client.command_handler(event)
```

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
    - saleh | rubika.ir/TheServer

_____________________________

Rubx - ⚡
========

  - Now the best ‍`sync‍` library for Rubik's was developed
  - ⭐️ Thanks **everyone** who has starred the project, it means a lot!

**Rubx** is an sync **Python 3** rubika library to interact with Rubika's API
as a user or through a bot account (self API alternative).

    🔴 If you have code using Rubx before its 8.0.5 version, you must
    read docs to learn how to migrate.

What is this?
-------------

Rubika is a popular messaging application. This library is meant
to make it easy for you to write Python programs that can interact
with Rubika. Think of it as a wrapper that has already done the
heavy job for you, so you can focus on developing an application.
This module provides all the desired methods with a very simple and beautiful user interface and has a very high speed.
Give your employer the best experience of a project.


Updating - 🌀
--------
The next updates include `async`, complete documentation and optimization.


# rubika client self with python3 RUBX module ![](https://i.imgur.com/fe85aVR.png)


_______________________

[![Python 3|2.7|3.x](https://img.shields.io/badge/python-3|3.0|3.x-yellow.svg)](https://www.python.org/)

[![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Mester-Root/rubx/main/LICENSE)

[![creator: ](https://img.shields.io/badge/Telegram-Channel-33A8E3)](https://t.me/rubx_library)

[![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/ClientUser)

_______________________


![issues](https://img.shields.io/github/issues/mester-root/rubx)

![forks](https://img.shields.io/github/forks/mester-root/rubx)

![stars](https://img.shields.io/github/stars/mester-root/rubx)

![license](https://img.shields.io/github/license/mester-root/rubx)

________________________


## the **special**:
- *[RUBX] > a library or module 'official' for rubika messnger with client server from iran ! for all .*
- *[RUBX] > full method .*
- *[RUBX] > rubika api's method for you .*


_________
مثال هایی که میتوانید استفاده کنید: - ✅
-------

[![EXAMPLES](https://raw.githubusercontent.com/Mester-Root/rubx/main/example.png)](https://github.com/Mester-Root/rubx/tree/main/Examples)
