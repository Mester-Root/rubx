# Rubx | Rubika Client Module

```python
from rb import Handler, EventBuilder, Filters, Performers

client = Handler(...)

# the funcs: `ChatsUpdates`, `MessagesUpdates`, `HandShake` # websocket

client.add_event_handling(func=Performers.hand_shake, events=dict(get_messages=True, get_chats=False))

@client.handler
def update(app: StartClient, message: EventBuilder, event):
    ... # code

```

:مقدمه
------
    - چت آیدی چیست؟
    - سشن چیست؟
    - auth, guid چیست؟

توضیحات:
-----
    
    - سشن یا auth کلید اکانت است که تمامی داده ها بر طبق آن رمزنگگاری میشوند.
    - چت آیدی یا guid ,آیدی عمومی اکانت ها است .که بصورت جی یو آیدی تلفظ میشود
