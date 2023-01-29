#!/bin/python

import logging
from datetime   import datetime
from os         import system
from re         import compile, findall, search, sub
from requests   import get
from rb         import (RubikaClient as Client, Handler,
                        EventBuilder, Filters, Performers) # rubx lib - 10.4.0 version

logging.basicConfig(level=logging.WARNING)


# inserts
SESSION         =   'abc...'        # account key [auth]
ADMINS          =   ['@username', ] # admin id
CREATORS        =   ['u0...', ]     # creator guid
DEFUALT_START   =   True


# info to use :
'''
# rubx module | Rubika Client API Framework

ADMINS:

    commands:
        - /sent or /send
        - /dl or !dl
        - /joiner

    switchs:
        - /sent [channel id or link] [file name] [caption] #checking with regex
        - /dl [url for downloading] [file name] [channel link] [caption] #checking with space
        - /joiner [channel link] #checking with regex

    examples:
        - /sent @theClient file.mp3 its a caption
        - /dl https://main-link.com/pages file.mp3 @theClient its a caption
        - /joiner @TheClient

CREATORS:

    commands:
        - /add
        - /del
        - /adminList
    
    switchs:
        - /add [user id]
        - /del [user id]
        - /adminList "dont swiths"
    
    examples:
        - /add @TheServer
        - /del @TheServer
        - /admin_list
'''


app, step = Client(SESSION), {}

if ('windows' in str(__import__('platform').system()).lower()):
    system('cls')
else:
    system('clear')

if not isinstance(ADMINS, list):
    ADMINS: list = [ADMINS]
if not isinstance(CREATORS, list):
    creators: list = [CREATORS]

# for infomration
class Info:
    admins, chat_ids, creators, now, links = ADMINS, [], CREATORS, True, []

# main class
class Get(object):

    # check link type [personal or public]
    @staticmethod
    def link_type(link: str) -> str:
        if link.startswith('@'):
            return 'pc'
        elif len(link) == 56 or len(link) == 56 - 8 and 'joinc' in link:
            return 'c'

    # check access channel [admin robot in channel]
    @staticmethod
    def checkAccess(guid: str) -> bool:
        if 'SendMessages' in app.get_chat_info(guid)['data']['chat']['access']:
            return False
        else:
            return True

    # send all files
    @staticmethod
    def sendFiles(link: str, fileFormat: str,
                  caption: str) -> ...:
        
        if '.mp3' in fileFormat.lower():

            for i in range(5):
                try:
                    (app / dict(chat_id=link, file=f'{fileFormat}', caption=caption))
                    break
                except Exception: pass

        elif '.mp4' in fileFormat.lower():

            for i in range(5):
                try:
                    (app // dict(chat_id=link, file=f'{fileFormat}', caption=caption))
                    break
                except Exception: pass

        elif '.png' in fileFormat.lower() or 'jpg' in fileFormat.lower():

            for i in range(5):
                try:
                    app.send_photo(link, f'{fileFormat}', caption=caption)
                    break
                except Exception: pass

        elif '.gif' in fileFormat.lower():
            for i in range(5):
                try:
                    app.send_gif(link, f'{fileFormat}', caption=caption)
                    break
                except Exception: pass
        
        elif '.null' in fileFormat.lower() or '.ogg' in fileFormat.lower():
            for i in range(5):
                try:
                    (app % dict(chat_id=link, file=f'{fileFormat}', caption=caption))
                    break
                except Exception: pass
        
        else:
            (app ** dict(chat_id=link, file=f'{fileFormat}', caption=caption))

    # get admin chat id [guid]
    @staticmethod
    def getAdmins() -> ...:
        
        try:
            if any('@' in admin for admin in Info.admins):
                
                for admin in Info.admins:
                    Info.chat_ids.append(str(app.get_object_by_username(str(admin.replace('@', '')))['data']['user']['user_guid']))
            else:
                Info.chat_ids: list = Info.admins
            
            for chat_id in Info.chat_ids:
                (app == dict(text=f'[📶] -> uploader robot onlined! in {str(datetime.now())[:19]}\n\nplz sent /help', chat_id=chat_id))
        
        except Exception:
            pass
    
    # detecting commands
    @staticmethod
    def replacer(mainText: str, mode='/send'):
        
        # mode send to return a list 2 index ['file name', 'channel link', 'caption']
        if '/send' in mode:
            mainText = mainText.replace('/send', '').replace('/sent', '')
            try:
                return [
                    findall(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', mainText)[0],
                    findall(r'(\@\w{4,20})', mainText)[0],
                    str(sub(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', '', str(sub(compile(r'(\@\w{3,20})'), '', mainText))))
                    ]
            except IndexError:
                try:
                    return [
                        findall(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', mainText)[0],
                        findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', mainText)[0],
                        str(sub(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', '', str(sub(compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'), '', mainText))))
                        ]
                except IndexError:
                    try:
                        return [
                            findall(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', mainText)[0],
                            findall(r'(rubika\.ir\/join[c,g]\/\w{32})', mainText)[0],
                            str(sub(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', '', str(sub(compile(r'(rubika\.ir\/join[c,g]\/\w{32})'), '', mainText))))
                            ]
                    except IndexError:
                        return [
                            findall(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', mainText)[0],
                            findall(r'(rubika\.ir/\w{4,20})', mainText)[0],
                            str(sub(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}', '', str(sub(compile(r'(rubika\.ir/\w{4,20})'), '', mainText))))
                            ]

        # for mode dl - download and upload. to return a dictionary {'download url': ..., 'file name': ..., 'channel link': ..., 'caption': ..., 'regCaption': ...}
        elif ('/dl' in mode or '!dl' in mode):
            
            realText: str = mainText.replace('/dl ', '').replace('!dl ', '')
            data: dict = {}
            textList: list = realText.split(' ')
            data['downloadUrl'] = textList[0]
            data['fileName'] = textList[1]
            data['channelLink'] = textList[2]
            try:
                caption: str = str(sub(compile(r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}'), '', realText))
                caption: str = str(sub(compile(r'\@\w{4,20}'), '', caption))
                caption: str = str(sub(compile(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}'), '', caption))
            except IndexError:
                caption: str = str(sub(compile(r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}'), '', realText))
                caption: str = str(sub(compile(r'[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.\w{3}'), '', caption))
            try:
                data['caption'] = ' '.join(textList[3:])
            except IndexError:
                data['caption'] = (textList[3])
            data['regCaption']: str = caption
            return (data)
        
        elif ('join' in mode):
            
            mainText: str = mainText.replace('!join', '').replace('/joiner', '')
            
            try:
                return (findall(r'(\@\w{4,20})', mainText)[0].replace('@', ''))
            except IndexError:
                try:
                    return (findall(r'(rubika\.ir/join[c,g]/\w{32})', mainText)[0])
                except IndexError:
                    try:
                        return (findall(r'(rubika\.ir/\w{4,20})', mainText)[0].replace('rubika.ir/', ''))
                    except IndexError:
                        return (mainText).replace('@', '')

# main function for run and starting self
def getChats(*args) -> ...:
    Get.getAdmins()
    
    try:
        with Handler(SESSION) as client:
            client.add_event_handling(func=Performers.chats_updates, events=dict(get_chats=True, get_messages=True))
            
            @client.handler
            def update(methods: Client, message: EventBuilder, event: dict):
                
                try:
                    
                    if DEFUALT_START and any(message.author_object_guid in user for user in Info.chat_ids) or message.author_object_guid in Info.creators:
                        
                        if message.raw_text == '/help':
                            message.respond('# rubx module | Rubika Client API Framework\n\nADMINS:\n    commands:\n        - / sent or / send\n        - / dl or ! dl\n        - / joiner\n\nswitchs:\n        - / sent [channel id or link] [file name] [caption] #checking with regex\n        - / dl [url for downloading] [file name] [channel link] [caption] #checking with space\n        - /joiner [channel link] #checking with regex\n\nexamples:\n        - / sent @theClient file.mp3 its a caption\n        - / dl https://main-link.com/pages file.mp3 @theClient its a caption\n        - / joiner @TheClient\n\n\nCREATORS:\n    commands:\n            - / add\n            - / del\n            - / admin_list\n\n    switchs:\n            - / add [user id]\n            - / del [user id]\n            - / admin_list "dont swiths"\n\n        examples:\n            - / add @TheServer\n            - / del @TheServer\n           - / admin_list')
                    
                        # to join in channel #just channel!
                        elif message.raw_text == '/joiner':
                            
                            resText: str = methods.get_messages_by_id(message.author_object_guid, [message.message_id]).get('data').get('messages')[0]['text']
                            command: str = Get.replacer(resText, 'join')
                            
                            try:
                                if '@' in resText:
                                    link: str = command
                                    link: str = methods.get_object_by_username(link)['data']['channel']['channel_guid']
                                    methods.join_channel_action(link)
                                    message.respond('[✅] -> robot joined!')
                                else:
                                    methods.join_channel_by_link(command)
                                    message.respond('[✅] -> robot joined!')

                            except IndexError:
                                message.respond('[❌] - command error.')
                            except Exception:
                                message.respond('[❌] - rubika client error. please try again!')
                            finally:
                                pass
                        
                        # to donwload from link and upload to channel
                        elif search(r'^\w{1}dl (\S+)$|\w{1}dl', message.raw_text):
                            
                            message.respond('just a moment...')
                            
                            try:
                                resText: str = methods.get_messages_by_id(message.author_object_guid, [message.message_id])['data']['messages'][0]['text']
                                command: dict = Get.replacer(mainText=str(resText), mode='/dl')
                                url: str = command['downloadUrl']
                                fileFormat: str = command['fileName']
                                link: str = command['channelLink']
                                caption: str = command['caption']
                                regCaption: str = command['regCaption']
                                
                                if '@' in link:
                                    link_uid: str = methods.get_object_by_username(link.replace('@', ''))['data']['channel']['channel_guid']
                                    methods.join_channel_action(link)
                                    Info.links.extend([link_uid])
                                
                                else:
                                    methods.join_channel_by_link(link)
                                    link_uid: str = (methods.channel_preview_by_join_link(link)['channel']['channel_guid'])
                                    Info.links.extend([link_uid])
                                
                                if Get.checkAccess(Info.links[0]):
                                    message.respond('[❌] - robot not admin in channel! please admin robot to channel and rty again.')
                                
                                else:
                                    message.respond('[🔄] - downloading...')
                                    
                                    with open(f'{fileFormat}', 'wb') as f:
                                        f.write(get(url).content)
                                        message.edit('[✅] -> url downloaded!')
                                    
                                    message.respond(f'[🔄] - uploading file...\n\nfile name: {fileFormat}\ndownload url: {url}\ncaption: {caption}\nregCaption: {regCaption}\n{"channel link" if not "@" in link else "channel ID"}: {link}\n\nyou: {"creator" if message.author_object_guid in Info.creators else "admin"}\nthe time start: {str(datetime.now())[:19]}\ntime end: 1 - 10 mins')
                                    Get.sendFiles(Info.links[0], fileFormat, caption)
                                    message.respond(f'[✅] -> file uploaded!\n\ndownload url: {url}\nfile name: {fileFormat}\nchannel link: {link}\ncaption: {caption}\n\nthe time: {str(datetime.now())[:19]}')
                                    Info.links.clear()
                            
                            except IndexError:
                                message.respond('[❌] - command error!')
                            except Exception:
                                message.respond('[❌] - rubika client error, please try again.')
                            finally:
                                pass
                        
                        # to download forwarded file and upload to channel
                        elif ('/send' in message.text or '/sent' in message.text):
                            
                            message.respond('just a moment ...')
                            
                            for text in methods.get_messages_interval(middle_message_id=(methods & message.author_object_guid), chat_id=message.author_object_guid).get('data').get('messages'):
                                
                                if (text['type'] == 'Text' and str(text.get('time'))[6] == str(int(datetime.today().timestamp()))[6]):
                                    
                                    if '/send' in text.get('text') or '/sent' in text.get('text') and 'reply_to_message_id' in text.keys():
                                        
                                        message.respond('[🆗] plz wait... ↺⟳')
                                        
                                        try:
                                            command: list = Get.replacer(mainText=str(text['text']), mode='/send')
                                            fileFormat: str = command[0]
                                            channel_link: str = command[1]
                                            caption: str = command[2]
                                            
                                            if Get.link_type(channel_link) == 'pc':
                                                link: str = methods.get_object_by_username(channel_link.replace('@', ''))['data']['channel']['channel_guid']
                                                methods.set_channel_action(link)
                                                Info.links.extend([link])
                                            
                                            elif Get.link_type(channel_link) == 'c':
                                                methods.join_channel_by_link(channel_link)
                                                link: str =  (methods.channel_preview_by_join_link(channel_link)['data']['channel']['channel_guid'])
                                                Info.links.extend([link])
                                            
                                            message.respond('[🔄] - checking channel...')
                                           
                                            if Get.checkAccess(Info.links[0]):
                                                
                                                message.respond('[❌] - robot is not admin to channel! please admin robot to channel and try again.')
                                            
                                            else:
                                                
                                                if 'forwarded_from' in methods.get_messages_by_id(text['author_object_guid'], [text['reply_to_message_id']])['data']['messages'][0].keys():
                                                    
                                                    message.respond(f'[🔄] - DOWNLOADING FILE...\n\nfile name: {fileFormat}\n{"channel link" if not "@" in channel_link else "channel ID"}: {channel_link}\ncaption: {caption}\n\nthe time: {str(datetime.now())[:19]}\nyou: {"creator" if message.author_object_guid in Info.creators else "admin"}\ntime end: 1 to 10 mins')
                                                    (methods - dict(download_type='message', save=True, save_as=text['text'].split(' ')[2], chat_id=text['author_object_guid'], message=text['reply_to_message_id']))
                                                    message.respond(f'[✅] -> FILE DOWNLOADED!')
                                                    message.respond(f'[🔄] - UPLOADING FILE...\n\nfile name : {fileFormat}\n{"channel link" if not "@" in channel_link else "channel ID"}: {channel_link}\ncaption: {caption}\n\nyou: {"creator" if message.author_object_guid in Info.creators else "admin"}\nthe time: {str(datetime.now())[:19]}')
                                                    Get.sendFiles(Info.links[0], fileFormat, caption)
                                                    message.respond(f'[✅] -> FILE UPLOADED!\nname: {fileFormat}')
                                                    Info.links.clear()
                                            
                                            break
                                        
                                        except IndexError:
                                            message.respond('[❌] - command error.')
                                        
                                        except Exception:
                                            message.respond('[❌] - rubika client error. please try again!')
                                        
                                        finally:
                                            pass

                        # to delete admin by creator
                        elif message.raw_text == '/del' and message.author_object_guid in Info.creators:
                            
                            try:
                                u_guid: str = methods.get_object_by_username(message.text.split(' ')[1].replace('@', ''))['data']['user']['user_guid']
                                
                                if u_guid in Info.admins:
                                    Info.chat_ids.remove(u_guid)
                                    message.respond(f'[✅] -> creator\n\n a admin deleted\nadmin guid: {u_guid}\nadmin id: {message.text.split(" ")[1]}', Filters.author)
                                    methods == dict(chat_id=u_guid, text=f'[🆗] -> شما از لیست ادمین های ربات توسط مالک حذف شدید.') # to send message
                                
                                else:
                                    message.respond(f'[❌] -> user dont admin.')
                            
                            except IndexError:
                                message.respond(f'[❌] - sorry, error in command.')
                            
                            except KeyError:
                                message.respond(f'[❌] - sorry, error in ID\n\nid is not a user.')
                            
                            except Exception:
                                message.respond(f'[❌] - sorry, rubika client error.')

                        # to add admin by creator
                        elif message.raw_text == '/add' and message.author_object_guid in Info.creators:
                            
                            try:
                                u_guid: str = methods.get_object_by_username(messagge.text.split(' ')[1].replace('@', ''))['data']['user']['user_guid']
                                
                                if not u_guid in Info.admins:
                                    Info.chat_ids.append(u_guid)
                                    message.respond(f'[✅] -> creator\n\n a user added\nadmin guid: {u_guid}\nadmin id: {message.text.split(" ")[1]}')
                                    methods == dict(chat_id=u_guid, text=f'[🆕] -> شما به لیست ادمین های ربات توسط مالک اضافه شدید.') 
                                else:
                                    message.respond('[!] -> user is admin.')
                            
                            except IndexError:
                                message.respond(f'[❌] - sorry, error in command.')
                            
                            except KeyError:
                                message.respond(f'[❌] - sorry, error in ID\n\nid is not a user.')
                            
                            except:
                                message.respond(f'[❌] - sorry, rubika client error.')

                        # for view admin list
                        elif message.raw_text == '/admin_list' and message.author_object_guid in Info.creators:
                            text: str = ''
                            for user in Info.chat_ids:
                                try:
                                    text += '@' + (methods * user)['data']['user']['username'] + '\n'
                                except KeyError:
                                    text += '@' + (methods * user)['data']['user']['first_name'] + '\n'
                            else:
                                message.respond(f'[✅] -> admin members list in [robot]:\n\n{text}\n\nyou: creator\nthe time: {str(datetime.now())[:19]}')

                        # to online robot
                        elif message.raw_text.upper() == '/ON' and message.author_object_guid in Info.creators:
                            if not Info.now:
                                Info.now: bool = True
                                message.respond(f'[✅] -> robot [onlined] 🕞\nfor off: /OFF\nyou: creator\nthe time: {str(datetime.now())[:19]}')
                            else:
                                message.respond(f'[!] -> ربات از قبل روشن است.', Filters.author)

                        # to offline robot
                        elif message.raw_text.upper() == '/OFF' and message.author_object_guid in Info.creators:
                            if Info.now:
                                Info.now: bool = False
                                message.respond(f'[✅] -> robot [offlined] 📴\nfor on: /ON\nyou: creator\nthe time: {str(datetime.now())[:19]}')
                            else:
                                message.respond(f'[!] -> ربات از قبل خاموش است.')

                except Exception: ...

    except KeyboardInterrupt:
        list(map(lambda creator: app == dict(text='[⏱] - robot stoped by user', chat_id=creator), creators))
        quit('stoped by user')

if __name__ == '__main__':
    getChats() # TODO: to use from threading or multithreading
