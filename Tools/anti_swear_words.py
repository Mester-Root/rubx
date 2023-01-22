from re import search

finder = lambda text, filters: any(bool(search(string, text)) for string in filters)

def parse(text: str, *args) -> bool:
  '''
  return an bool to detecting badwords in text
  '''
  return finder(text, ['bad', 'swear', 'unlike', 'fuck'])

print(parse('Hello bad and dad fucker'))

# Examples

'''
from rb import Handler, Filters, Performers

client = Handler('session')

def event(update):
    if parse(update.message.text):
        message.delete()
        # message.delete([update.message.message_id], update.object_guid)
        # message.delete([update.message.message_id], update.message.author_object_guid)

client.add_event_handling(Performers.hand_shake, event=dict(get_chats=False, get_messages=True))
client.start = True
client.command_handler(event)
'''
