#!/bin/python
# echo bot
# rubx lib v 10.1.9
from rb import Handler, EventBuilder, Filters

client = Handler(...) # insert session

client.add_event_handling(func='ChatsUpdates', events=dict()) # ChatsUpdates for getting all updates.

@client.handler
def update(app, message: EventBuilder, event: dict):
    message.respond(message.text, Filters.chat) # Filters chat to all object