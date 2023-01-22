#!/bin/python

def anti_spam(texts: list) -> dict:
    '''
    anti_spam(['Hey', 'Love', 'Hey'])
    '''

    result: dict = {'spam_index_list': []}

    for text, index in zip(texts, range(len(texts))):
        texts.remove(text)
        list(map(lambda text: result['spam_index_list'].append(index), texts))

    else:
        if len(result.get('spam_index_list')) >= 1:
            result.update({'is_spam': True})
        return result

    #list(map(lambda text: (indexs.extend(texts.index(text)), texts.remove(text)) if texts.count(text) > 2 else ..., texts))

# TO USE
print(anti_spam(['Hey', 'Love', 'Hey']))

# Examples

'''
from rb import Handler, Filters, Performers, EventBuilder, BaseClient

client = Handler('session')
client.add_event_handling(func=Performers.hand_shake, events=dict(get_messages=True, get_chats=False))

@client.handler
def update(client, message, event):
    updates: list = []
    updates.append((message.message.text, message.message.message_id))
    if len(updates) >= 3:
        print(anti_spam(updates))
        ...
# Or

async def run(*args):
    async with BaseClient('session') as client:
        results = await client.start(client.get_messages_interval, chat_id='g0...', middle_message_id=await client.start(client.get_chat_last_message_id('g0...')))
        finded = anti_spam([text.get('text') for text in results['data']['messages']])
        if finded.get('is_spam'):
            for i in finded['spam_index_list']:
                await client.start(client.delete_messages, [results['data']['messages'][i].get('message_id')], 'g0...')
BaseClient.run(run)
'''
