#!/bin/python
# rubika api bot methods

from .connection import GetData as http, Connection
import re, typing, logging


class BotMethods:


    def __enter__(self):
        return self


    def __exit__(self, *args, **kwargs):
        pass


    @classmethod
    def method(cls, token: str,
               method: str, **data) -> typing.Union[dict, str]:
        
        '''
        this method has for use from api bot to custom
        
        `self.method('token', 'sendMessage', chat_id=..., text=...)` # and other methods ...
        '''
        
        return http.bot(token=token, method=method, data=data)


    @property
    def get_me(self) -> typing.Union[dict, str]:
        '''
        getting your bot session
        
        `print(self.get_me)`
        '''
        
        return http.bot(token=self.token, method='getMe', data={})


    def get_chat(self, chat_id: str,
                 *args, **kwargs) -> typing.Union[str, dict]:
        
        '''
        get all message from a chat
        
        `self.get_chat('chat-id')`
        '''
        
        return http.bot(token=self.token, method='getChat', data={'chat_id': chat_id})


    def get_updates(self,
                    limit: int = 10,
                    offset_id: typing.Optional[str] = None,
                    *args,
                    **kwargs) -> typing.Union[str, dict]:
        
        '''
        `self.get_updates(1) # get last message`
        '''
        
        data: dict = {'limit': limit}.update({'offset_id': offset_id}) if offset_id else {'limit': limit}

        return http.bot(token=self.token, method='getUpdates', data=data)


    def update_bot_endpoint(
        self,
        url: str,
        types: typing.Literal['ReceiveUpdate', 'ReceiveInlineMessage',
                      'ReceiveQuery', 'GetSelectionItem',
                      'SearchSelectionItems']
        ) -> typing.Union[str, dict]:
        
        '''
        `self.update_bot_endpoint(...)`
        '''

        return http.bot(token=sslf.token, method='updateBotEndpoints', data={'url': url, 'type': types})


    def send_message(
        self,
        chat_id             : str,
        text                : str,
        chat_keypad         : str = None,
        disable_notification: bool = False,
        inline_keypad       : str = None,
        reply_to_message_id : str = None,
        chat_keypad_type    : typing.Literal['Remove', 'New', None] = None) -> typing.Union[str, dict]:
        
        '''
        this method for send message
        
        `self.send_message('chat-id', 'Hey!')`
        '''
        
        data: dict = {
            'text'                  :   text,
            'chat_id'               :   chat_id,
            'chat_keypad'           :   chat_keypad,
            'inline_keypad'         :   inline_keypad,
            'chat_keypad_type'      :   chat_keypad_type,
            'reply_to_message_id'   :   reply_to_message_id,
            'disable_notification'  :   disable_notification
            }

        return http.bot(token=self.token, method='sendMessage', data=data)


    def delete_message(self,
                       chat_id: str,
                       message_id: str) -> typing.Union[str, dict]:
        
        '''
        `self.delete_message('chat-id', '1234...') # delete a message from chat`
        '''
        
        return http.bot(token=self.token, method='delteMessage', data={'chat_id': chat_id, 'message_id': message_id})


    def forward_message(
        self,
        from_chat_id        : str,
        message_id          : str,
        to_chat_id          : str,
        disable_notification: bool = False
        ) -> typing.Union[str, dict]:
        
        '''
        `self.forward_message('f chat-id', '1234...', 't chat-id', True) # TODO: forward a message`
        '''
        
        data: dict = {
            'from_chat_id'          :   from_chat_id,
            'message_id'            :   message_id,
            'to_chat_id'            :   to_chat_id,
            'disable_notification'  :   disable_notification,
        }
        
        return http.bot(token=self.token, method='forwardMessage', data=data)


    def edit_message_text(self, chat_id: str,
                          message_id: str, text: str) -> typing.Union[str, dict]:
        
        '''
        `self.edit_message_text('chat-id', '1234...', 'new-event') # TODO: edit message for text type`
        '''
        
        data: dict = {
            'text'      :   text,
            'chat_id'   :   chat_id,
            'message_id':   message_id
            }

        return http.bot(token=self.token, method='editMessageText', data=data)


    def edit_message_keypad(self: 'BotMethods',
                            chat_id: str,
                            message_id: str,
                            inline_keypad: dict,
                            *args, **kwargs) -> typing.Union[str, dict]:
        
        '''
        `self.edit_message_keypad('chat-id', '1234...', {}) # TODO: edit message keypad`
        '''
        
        data: dict = {
            'chat_id'       :   chat_id,
            'message_id'    :   message_id,
            'inline_keypad' :   inline_keypad
            }

        return http.bot(token=self.token, method='editMessageKeypad', data=data)


    def edit_chat_keypad(
        self,
        chat_id         : str,
        chat_keypad     : dict = None,
        chat_keypad_type: typing.Literal['New', 'Remove'] = 'Remove',
        *args,
        **kwargs
        ) -> typing.Union[str, dict]:

        '''
        `self.edit_chat_keypad('chat-id'. chat_keypad_type='Remove') # TODO: remove`
        '''
        
        data: dict = {
            'chat_id'           :   chat_id,
            'chat_keypad_type'  :   chat_keypad_type,
            } if not chat_keypad else {'chat_id': chat_id, 'chat_keypad_type': chat_keypad_type, 'chat_keypad': chat_keypad}


        return http.bot(token=self.token, method='editChatKeypad', data=data)


    def send_poll(
        self,
        chat_id                 : str,
        question                : str,
        options                 : typing.List[str],
        chat_keypad             : dict = None,
        disable_notification    : bool = False,
        inline_keypad           : dict = None,
        reply_to_message_id     : typing.Optional[str] = None,
        chat_keypad_type        : typing.Literal[None, 'New', 'Remove'] = None
        ) -> typing.Union[dict, str]:
        
        '''
        this method for send poll (question)
        
        `self.send_poll('chat-id', 'how r u?', ['fine', 'bad'])`
        '''
        
        data: dict = {
            'chat_id'               :   chat_id,
            'options'               :   options,
            'question'              :   question,
            'chat_keypad'           :   chat_keypad,
            'inline_keypad'         :   inline_keypad,
            'chat_keypad_type'      :   chat_keypad_type,
            'reply_to_message_id'   :   reply_to_message_id,
            'disable_notification'  :   disable_notification
            }
        
        return http.bot(token=self.token, method='sendPoll', data=data)


    def send_location(
        self,
        token               : str,
        chat_id             : str,
        latitude            : str,
        longitude           : str,
        chat_keypad         : dict = None,
        disable_notification: bool = False,
        inline_keypad       : dict = None,
        reply_to_message_id : typing.Optional[str] = None,
        chat_keypad_type    : typing.Literal[None, 'New', 'Remove'] = None,
        ) -> typing.Union[str, dict]:
        
        '''
        this method has for send location
        
        `self.send_location('chat-id', ...)`
        '''
        
        data: dict = {
            'chat_id'               :   chat_id,
            'latitude'              :   latitude,
            'longitude'             :   longitude,
            'chat_keypad'           :   chat_keypad,
            'disable_notification'  :   disable_notification,
            'inline_keypad'         :   inline_keypad,
            'reply_to_message_id'   :   reply_to_message_id,
            'chat_keypad_type'      :   chat_keypad_type
            }
        
        return http.bot(token=self.token, method='sendLocation', data=data)


    def send_sticker(
        self,
        chat_id             : str,
        sticker_id          : str,
        chat_keypad         : dict = None,
        disable_notification: bool = False,
        inline_keypad       : dict = None,
        reply_to_message_id : typing.Optional[str] = None,
        chat_keypad_type    : typing.Literal[None, 'New', 'Remove'] = None
        ) -> typing.Union[str, dict]:
        
        '''
        sent a sticker to chat
        
        `self.send_sticker('chat-id', 's-id')`
        '''
        
        data: dict = {
            'chat_id'               :   chat_id,
            'sticker_id'            :   sticker_id,
            'chat_keypad'           :   chat_keypad,
            'disable_notification'  :   disable_notification,
            'inline_keypad'         :   inline_keypad,
            'reply_to_message_id'   :   reply_to_message_id,
            'chat_keypad_type'      :   chat_keypad_type
            }
        
        return http.bot(token=self.token, method='sendSticker', data=data)


    def send_contact(
        self,
        chat_id             : str,
        first_name          : str,
        last_name           : str,
        phone_number        : str,
        chat_keypad         : dict = None,
        disable_notification: bool = False,
        inline_keypad       : dict = None,
        reply_to_message_id : typing.Optional[str] = None,
        chat_keypad_type    : typing.Literal[None, 'New', 'Remove'] = None
        ) -> typing.Union[str, dict]:
        
        data: dict = {
            'chat_id'               :   chat_id,
            'last_name'             :   last_name,
            'first_name'            :   first_name,
            'chat_keypad'           :   chat_keypad,
            'phone_number'          :   phone_number,
            'inline_keypad'         :   inline_keypad,
            'chat_keypad_type'      :   chat_keypad_type,
            'reply_to_message_id'   :   reply_to_message_id,
            'disable_notification'  :   disable_notification
            }
        
        return http.bot(token=self.token, method='sendContact', data=data)


    def __request_send_file(
        self,
        types: typing.Literal['File', 'Image',
                               'Voice', 'Music', 'Gif']
        ) -> typing.Union[str, dict]:
        
        '''
        get url upload file from api
        
        `self.__request_send_file('Music') # return a dict or attr for get url`
        '''
        
        return http.bot(token=self.token, method='requestSendFile', data={'type': types})


    def send_files(
        self,
        chat_id             :   str,
        file                :   str                                                      = None,
        file_type           :   typing.Literal['File', 'Image', 'Voice', 'Music', 'Gif'] = 'File',
        chat_keypad         :   dict                                                     = None,
        disable_notification:   bool                                                     = False,
        inline_keypad       :   dict                                                     = None,
        reply_to_message_id :   typing.Optional[str]                                     = None,
        chat_keypad_type    :   typing.Literal[None, 'New', 'Remove']                    = None
        ) -> typing.Union[str, dict]:


        '''
        # this method has for sending all format type file
        ## make uploading
        
        chat_id: object id
        
        file: file path
        
        file_type: for file action type = 'File', 'Image', 'Voice', 'Music', 'Gif'
        
        chat_keypad: {'rows': {'buttons': []}, 'resize_keyboard': False, 'on_time_keyboard': True}
        
        disable_notification: for see user notif: False, True
        
        inline_keypad: chat_keypad inline
        
        reply_to_message_id: for reply to a message
        
        chat_keypad_type: if u usage chat_keypad: insert action type: 'New', 'Remove'


        # Use:
            - `self.send_files('chat-guid', 'C:\\music.mp3', 'Music')` 
        '''

        url = self.__request_send_file(file_type or 'File')
        file_id = self.__upload(url, file)

        data: dict = {
            'chat_id'               :   chat_id,
            'file_id'               :   file_id,
            'chat_keypad'           :   chat_keypad,
            'disable_notification'  :   disable_notification,
            'inline_keypad'         :   inline_keypad,
            'reply_to_message_id'   :   reply_to_message_id,
            'chat_keypad_type'      :   chat_keypad_type
            }
        
        return http.bot(token=self.token, method='sendFile', data=data)


    def __upload(self, url: str, file_name: str,
               file_path: str = None, *args, **kwargs) -> typing.Union[str, dict]:
        
        '''
        get file id from url
        
        `self.__upload('url', 'C:/file.mp3')`
        '''
        
        return http.bot('file', token=self.token, data={'file': (file_name.split('\\')[-1] if file_name.__contains__('\\') else file_name.split('/')[-1] if file_name.__contains__('/') else file_name, open(file_path or file_name, 'rb+'))}, url=url)


    def download(self, file_id: str) -> typing.Union[str, dict]:
        '''
        downloading file from id
        
        `self.download('file-id')`
        '''
        
        return http.bot(token=self.token, method='getFile', data={'file_id': file_id})


    def get_file(self, file_id: str,
                 *args, **kwargs) -> typing.Union[str, dict]:
        
        '''
        downloading file from id
        
        `self.get_file('file-id')`
        '''
        
        return self.download(file_id)


    def set_commands(self, bot_commands: typing.List[str],
                     *args, **kwargs) -> typing.Union[str, dict]:
        
        '''
        `self.set_commands([str]) # TODO: set bot commands`
        '''
        
        return http.bot(token=self.token, method='setCommands', data={'bot_commands': bot_commands})


    def on(self) -> None:
        pass
