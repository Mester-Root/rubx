#!/bin/python

from datetime import datetime
from os import system
from platform import system as sysType
from re import (compile, findall,
                search, sub)
from requests import get
from rb import StartClient as Client

# inserts
session     =   '' # account key
admins      =   ['@username', ] # admin id
creators    =   ['u0...', ] # creator guid

# file paths
MESSAGE_IDS = 'msgs.txt'


# info to use :
'''
admins:

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

creators:

    commands:
        - /add
        - /del
        - /adminList
    
    swiths:
        - /add [user id]
        - /del [user id]
        - /adminList "dont swiths"
    
    example:
        - /add @TheServer
        - /del @TheServer
        - /adminList
'''


open(MESSAGE_IDS, 'w')

app: Client = Client(
    session
    )

if ('Windows' in str(sysType())):
    system('cls')
else:
    system('clear')

if not isinstance(admins, list):
    admins: list = [admins]
if not isinstance(creators, list):
    creators: list = [creators]

# for infomration
class Info:
    admins, chat_ids, msg_id_blocks, creators, now, links = admins, [], open(MESSAGE_IDS, 'r+').read().split('\n'), creators, True, []

# main class
class Get(object):

    # check link type [personal or public]
    @staticmethod
    def link_type(
        link: str
        ) -> str:
        if link.startswith(
            '@'
            ):
            return 'pc'
        elif len(
            link
            ) == 56 or len(link) == 56 - 8 and 'joinc' in link:
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
    def sendFiles(
        link: str,
        fileFormat: str,
        caption: str
        ) -> ...:
        
        if '.mp3' in fileFormat.lower():
            try:
                for i in range(10):
                    try:
                        app.send_music(link, f'{fileFormat}', caption=caption)
                        break
                    except Exception: pass
            except Exception:
                pass
            
        elif '.mp4' in fileFormat.lower():
            try:
                for i in range(10):
                    try:
                        app.send_movie(link, f'{fileFormat}', caption=caption)
                        break
                    except Exception: pass
            except Exception: pass
            
        elif '.png' in fileFormat.lower() or 'jpg' in fileFormat.lower():
            
            try:
                for i in range(10):
                    try:
                        app.send_photo(link, f'{fileFormat}', caption=caption)
                        break
                    except Exception: pass
            except Exception: pass
            
        elif '.gif' in fileFormat.lower():
            for i in range(10):
                try:
                    app.send_gif(link, f'{fileFormat}', caption=caption)
                    break
                except Exception: pass
        else:
            app.send_document(link, f'{fileFormat}', caption=caption)
    
    # append message_ids to black list
    @staticmethod
    def append_to_blacks(
        message_id: str
        ) -> ...:
        if not message_id in open(MESSAGE_IDS, 'r').read():
            with open(MESSAGE_IDS, 'a+') as f:
                f.write(str(message_id)+'\n')

    # check message_id for msg ids blocked
    #def checkMsg(message_id: str) -> bool:
    checkMsg = lambda message_id: list(filter(lambda msg: msg in message_id, open(MESSAGE_IDS, 'r').read().split('\n')))

    # get admin chat id [guid]
    @staticmethod
    def getAdmins() -> ...:
        try:
            if any('@' in admin for admin in Info.admins):
                for admin in Info.admins:
                    Info.chat_ids.append(str(app.get_object_by_username(str(admin.replace('@', '')))['data']['user']['user_guid']))
            else: Info.chat_ids: list = Info.admins
            for chat_id in Info.chat_ids:
                app.send_message(text=f'[📶] -> robot onlined! in {str(datetime.now())[:19]}', chat_id=chat_id)
        except: pass
    
    # detecting commands
    @staticmethod
    def replacer(
        mainText: str,
        mode='/send'
        ):
        
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
        elif '/dl' in mode or '!dl' in mode:
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
        
        elif (
            'join'
            in
            mode
            ):
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
def getChats() -> ...:
    
    Get.getAdmins()
    print('robot started')
    
    while 1:
        try:
            for msg in (app.get_chats_updates().get('data').get('chats')): # geting chats text
                # TODO: use checker message id with filter:
                #if msg['abs_object']["type"] == "User" and msg['last_message']['type'] == 'Text' and not await Get().checkMsg(msg['last_message']['message_id']):
                
                if msg['abs_object']['type'] == 'User' and msg['last_message']['type'] == 'Text' and not any(str(msg['last_message']['message_id']) in black for black in Info.msg_id_blocks):
                    
                    # to join in channel #just channel!
                    if msg['last_message']['text'].startswith('/joiner') and any(str(msg['last_message']['author_object_guid']) in str(chat_guid) for chat_guid in Info.chat_ids) and Info.now:
                        resText: str = app.get_messages_by_id(msg['last_message']['author_object_guid'], [msg['last_message']['message_id']]).get('data').get('messages')[0]['text']
                        command: str = Get.replacer(resText, 'join')
                        try:
                            if '@' in resText:
                                link: str = command
                                link: str = app.get_object_by_username(link)['data']['channel']['channel_guid']
                                app.join_channel_action(link)
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[✅] -> robot joined!', reply_to_message_id=msg['last_message']['message_id'])
                            else:
                                app.join_channel_by_link(command)
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[✅] -> robot joined!', reply_to_message_id=msg['last_message']['message_id'])
                            
                            Get.append_to_blacks(msg['last_message']['message_id'])
                        except IndexError:
                            app.send_message(text='[❌] - command error.', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                        except Exception:
                            app.send_message(text='[❌] - rubika client error. please try again!', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                        finally:
                            pass
                    
                    # to donwload from link and upload to channel
                    elif search(r'\w{1}dl (\S+)$', msg['last_message']['text']) or msg['last_message']['text'].startswith('/dl') and any(msg['last_message']['author_object_guid'] in chat_guid for chat_guid in Info.chat_ids) and Info.now:
                        try:
                            resText: str = app.get_messages_by_id(msg['last_message']['author_object_guid'], [msg['last_message']['message_id']])['data']['messages'][0]['text']
                            command: dict = Get.replacer(mainText=str(resText), mode='/dl')
                            url: str = command['downloadUrl']
                            fileFormat: str = command['fileName']
                            link: str = command['channelLink']
                            caption: str = command['caption']
                            regCaption: str = command['regCaption']
                            if '@' in link:
                                link_uid: str = app.get_object_by_username(link.replace('@', ''))['data']['channel']['channel_guid']
                                app.join_channel_action(link)
                                Info.links.extend([link_uid])
                            else:
                                app.join_channel_by_link(link)
                                link_uid: str = (app.channel_preview_by_join_link(str(link))['channel']['channel_guid'])
                                Info.links.extend([link_uid])
                            if Get.checkAccess(Info.links[0]):
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[❌] - robot not admin in channel! please admin robot to channel and rty again.', reply_to_message_id=msg['last_message']['message_id'])
                            else:
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[🔄] - downloading...', reply_to_message_id=msg['last_message']['message_id'])
                                with open(f'{fileFormat}', 'wb') as f:
                                    f.write(get(url).content)
                                    app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[✅] -> url downloaded!', reply_to_message_id=msg['last_message']['message_id'])
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[🔄] - uploading file...\n\nfile name: {fileFormat}\ndownload url: {url}\ncaption: {caption}\nregCaption: {regCaption}\n{"channel link" if not "@" in link else "channel ID"}: {link}\n\nyou: {"creator" if msg["last_message"]["author_object_guid"] in Info.creators else "admin"}\nthe time start: {str(datetime.now())[:19]}\ntime end: 1 - 10 mins', message_id=msg['last_message']['message_id'])
                                (Get.sendFiles(Info.links[0], fileFormat, caption))
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> file uploaded!\n\ndownload url: {url}\nfile name: {fileFormat}\nchannel link: {link}\ncaption: {caption}\n\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=msg['last_message']['message_id'])
                                Info.links.clear()
                            Get.append_to_blacks(msg['last_message']['message_id'])
                        except IndexError:
                            app.send_message(text='[❌] - command error.', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                        except Exception:
                            app.send_message(text='[❌] - rubika client error. please try again!', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                        finally:
                            pass
                    
                    # to download forwarded file and upload to channel
                    elif msg['last_message']['text'].startswith('/sent') or msg['last_message']['text'].startswith('/send') and msg['last_message']['author_object_guid'] in Info.chat_ids and Info.now:
                        
                        for text in app.get_messages_interval(chat_id=msg['last_message']['author_object_guid'], middle_message_id=app.get_chat_info(msg['last_message']['author_object_guid'])['data']['chat']['last_message_id']).get('data').get('messages'):
                            
                            if (
                                text['type'] == 'Text'
                                and
                                str(text.get('time'))[6] == str(int(datetime.today().timestamp()))[6]
                                ):
                                if text['text'].startswith('/sent') or text['text'].startswith('/send') and 'reply_to_message_id' in text.keys() and not any(text['message_id'] in word for word in Info.msg_id_blocks):
                                    
                                    app.send_message('[🆗] plz wait... ↺⟳', text.get('author_object_guid'), reply_to_message_id=text.get('message_id'))
                                    
                                    try:
                                        command: list = Get.replacer(mainText=str(text['text']), mode='/send')
                                        fileFormat: str = command[0]
                                        channel_link: str = command[1]
                                        caption: str = command[2]
                                        
                                        if Get.link_type(channel_link) == 'pc':
                                            link: str = app.get_object_by_username(channel_link.replace('@', ''))['data']['channel']['channel_guid']
                                            app.set_channel_action(link)
                                            Info.links.extend([link])
                                        
                                        elif Get.link_type(channel_link) == 'c':
                                            app.join_channel_by_link(channel_link)
                                            link: str =  (app.channel_preview_by_join_link(channel_link)['data']['channel']['channel_guid'])
                                            Info.links.extend([link])
                                        
                                        app.send_message(text='[🔄] - checking channel...', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                                        
                                        if Get.checkAccess(Info.links[0]):
                                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text='[❌] - robot is not admin to channel! please admin robot to channel and try again.', reply_to_message_id=msg['last_message']['message_id'])
                                        
                                        else:
                                            if 'forwarded_from' in app.get_messages_by_id(text['author_object_guid'], [text['reply_to_message_id']])['data']['messages'][0].keys():
                                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[🔄] - DOWNLOADING FILE...\n\nfile name: {fileFormat}\n{"channel link" if not "@" in channel_link else "channel ID"}: {channel_link}\ncaption: {caption}\n\nthe time: {str(datetime.now())[:19]}\nyou: {"creator" if msg["last_message"]["author_object_guid"] in Info.creators else "admin"}\ntime end: 1 to 10 mins', reply_to_message_id=msg['last_message']['message_id'])
                                                app.get_file('message', True, saveAs=text['text'].split(' ')[2], chat_id=text['author_object_guid'], reply_to_message=text['reply_to_message_id'])
                                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> FILE DOWNLOADED!', reply_to_message_id=text['reply_to_message_id'])
                                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[🔄] - UPLOADING FILE...\n\nfile name : {fileFormat}\n{"channel link" if not "@" in channel_link else "channel ID"}: {channel_link}\ncaption: {caption}\n\nyou: {"creator" if msg["last_message"]["author_object_guid"] in Info.creators else "admin"}\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=text['reply_to_message_id'])
                                                Get.sendFiles(Info.links[0], fileFormat, caption)
                                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> FILE UPLOADED!\nname: {fileFormat}', reply_to_message_id=text['message_id'])
                                                Info.links.clear()
                                        break
                                    except IndexError or KeyError:
                                        app.send_message(text='[❌] - command error.', chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                                    
                                    except Exception as e:
                                        app.send_message(text='[❌] - rubika client error. please try again!\n\nerror: %s' % e, chat_id=msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                                    finally:
                                        pass
                                    
                                Get.append_to_blacks(msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # to delete admin by creator
                    elif msg['last_message']['text'].startswith('/del') and msg['last_message']['author_object_guid'] in Info.creators and Info.now:
                        try:
                            u_guid: str = app.get_object_by_username(msg['last_message']['text'].split(' ')[1].replace('@', ''))['data']['user']['user_guid']
                            if u_guid in Info.admins:
                                Info.chat_ids.remove(u_guid)
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> creator\n\n a admin deleted\nadmin guid: {u_guid}\nadmin id: {msg["last_message"]["text"].split(" ")[1]}', reply_to_message_id=msg['last_message']['message_id'])
                                app.send_message(chat_id=u_guid, text=f'[🆗] -> شما از لیست ادمین های ربات توسط مالک حذف شدید.')
                            else:
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] -> user dont admin.', reply_to_message_id=msg['last_message']['message_id'])
                        except IndexError:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, error in command.', reply_to_message_id=msg['last_message']['message_id'])
                        except KeyError:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, error in ID\n\nid is not a user.', reply_to_message_id=msg['last_message']['message_id'])
                        except:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, rubika client error.', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # to add admin by creator
                    elif msg['last_message']['text'].startswith('/add') and msg['last_message']['author_object_guid'] in Info.creators and Info.now:
                        try:
                            u_guid: str = app.get_object_by_username(msg['last_message']['text'].split(' ')[1].replace('@', ''))['data']['user']['user_guid']
                            if not u_guid in Info.admins:
                                Info.chat_ids.append(u_guid)
                                app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> creator\n\n a user added\nadmin guid: {u_guid}\nadmin id: {msg["last_message"]["text"].split(" ")[1]}', reply_to_message_id=msg['last_message']['message_id'])
                                app.send_message(chat_id=u_guid, text=f'[🆕] -> شما به لیست ادمین های ربات توسط مالک اضافه شدید.') 
                            else:
                                app.send_message('[!] -> user is admin.', msg['last_message']['author_object_guid'], reply_to_message_id=msg['last_message']['message_id'])
                        except IndexError:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, error in command.', reply_to_message_id=msg['last_message']['message_id'])
                        except KeyError:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, error in ID\n\nid is not a user.', reply_to_message_id=msg['last_message']['message_id'])
                        except:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[❌] - sorry, rubika client error.', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # for view command list and switchs
                    elif msg['last_message']['text'] == '/commands' and msg['last_message']['author_object_guid'] in Info.admins:
                        app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> ok, command list:\n\n/dl [url] [channel-link] [file-name]\n/send [channel-link] [file-name]\n!join [channel-link]\n\nfor creator:\n\n-    /add @username\n-    /del @username\n-    /adminList\n\nyou: creator\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # for view admin list
                    elif msg['last_message']['text'].startswith('/adminList') and msg['last_message']['author_object_guid'] in Info.creators and Info.now:
                        text: str = ''
                        for user in Info.chat_ids:
                            try:
                                text += '@' + app.get_chat_info(user)['data']['user']['username'] + '\n'
                            except KeyError:
                                text += '@' + app.get_chat_info(user)['data']['user']['first_name'] + '\n'
                        else:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> admin members list in [robot]:\n\n{text}\n\nyou: creator\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # to online robot
                    elif msg['last_message']['text'] == ('/ON') and msg['last_message']['author_object_guid'] in Info.creators:
                        if not Info.now:
                            Info.now: bool = True
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> robot [onlined] 🕞\nfor off: /OFF\nyou: creator\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=msg['last_message']['message_id'])
                        else:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[!] -> ربات از قبل روشن است.', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])
                    
                    # to offline robot
                    elif msg['last_message']['text'].startswith('/OFF') and msg['last_message']['author_object_guid'] in Info.creators:
                        if Info.now:
                            Info.now: bool = False
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[✅] -> robot [offlined] 📴\nfor on: /ON\nyou: creator\nthe time: {str(datetime.now())[:19]}', reply_to_message_id=msg['last_message']['message_id'])
                        else:
                            app.send_message(chat_id=msg['last_message']['author_object_guid'], text=f'[!] -> ربات از قبل خاموش است.', reply_to_message_id=msg['last_message']['message_id'])
                        Get.append_to_blacks(msg['last_message']['message_id'])

                    Get.append_to_blacks(msg['last_message']['message_id']) # TODO: delete this code

        except KeyboardInterrupt:
            list(map(lambda creator: app.send_message('[⏱] - robot stoped by user', creator), creators))
            quit('stoped by user')
        except Exception: ...

if __name__ == '__main__':
    __import__('threading').Thread(target=getChats()).start() # TODO: to use from threading or multithreading
