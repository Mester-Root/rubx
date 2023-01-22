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

=========

starting

=========

:مقدمه
------
    - چت آیدی چیست؟
    - سشن چیست؟
    - auth, guid چیست؟

توضیحات:
-----
    
    - سشن یا auth کلید اکانت است که تمامی داده ها بر طبق آن رمزنگاری میشوند.
    - چت آیدی یا guid ,آیدی عمومی اکانت ها است .که بصورت جی یو آیدی تلفظ میشود


________________
##### برای آغاز کار ابتدا بایستی پایتون را در سطح متوسط بلد باشید.

### شروع سریع


##### پکیج اصلی ای که باید محتویات را از آن وارد کنید:‌ `rb` نام دارد.
##### برای مثال به این صورت کلاس StartClient که برای پیامرسان است را وارد کنید:

```python
from rb import StartClient
```

##### توجه کنید تمامی متد های این کلاس بصورت `sync` میباشد.

#### پارامتر های کلاس StartClient:
```python
session_key: برای وارد کردن کلید اکانت شما.
chat_id: برای وارد کردن چت آیدی شما
username: برای وارد کردن یوزنیم (آیدی) شما
توضیحات بیشتر در باره تمامی پارامتر ها بزودی ...


### اکنون شروع پیامرسانی

##### برای ارسال یک پیام با کتابخانه شما میبایست چت آیدی تارگت خود را داشته باشید, برای اینکار به روبیکا وب مراجعه کرده و اطلاعات مورد نیاز را به دست آورید, یا از ربات های نوشته شده استفاده کنید.
##### متوانید اینکار را با یوزرنیم تارگت خود هم انجام دهید. اما استفاده از چت آیدی بسیار بهینه و بهتر است.

#### مثال:

```python
from rb import StartClient

client = StartClient('session')

print(client.send_message('سلام', 'chat-id'))
```

##### شما میتوانید سشن اکانت خود را از روبیکا وب بدست آورید; یا از اپ خودتون کپچر بگیرید.
#### همچنین این متد مهم یک میانبر هم دارد. توجه کنید:

```python
from rb import StartClient

client = StartClient('session')

print(client == dict(chat_id='chat-id', text='سلام'))
```

##### با استفاده از == بعد از آوردن سلف (کلاس وارد شده) متوانید به method ارسال پیام دسترسی داشته باشید.

