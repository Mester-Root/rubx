#!/bin/python

import struct
import typing
import os
from datetime import datetime, date, timedelta, timezone
from re import compile, escape, search, findall, sub
from time import sleep, gmtime, localtime
from base64 import b64encode
from collections import deque
from html.parser import HTMLParser

_EPOCH_NAIVE = datetime(*gmtime(0)[:6])
_EPOCH_NAIVE_LOCAL = datetime(*localtime(0)[:6])
_EPOCH = _EPOCH_NAIVE.replace(tzinfo=timezone.utc)

def _datetime_to_timestamp(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    secs = int((dt - _EPOCH).total_seconds())
    return struct.unpack('i', struct.pack('I', secs & 0xffffffff))[0]

def _json_default(value):
    if isinstance(value, bytes):
        return b64encode(value).decode('ascii')
    elif isinstance(value, datetime):
        return value.isoformat()
    else:
        return repr(value)

class TLObject:
    CONSTRUCTOR_ID = None
    SUBCLASS_OF_ID = None

    @staticmethod
    def pretty_format(obj, indent=None):
        if indent is None:
            if isinstance(obj, TLObject):
                obj = obj.to_dict()

            if isinstance(obj, dict):
                return '{}({})'.format(obj.get('_', 'dict'), ', '.join(
                    '{}={}'.format(k, TLObject.pretty_format(v))
                    for k, v in obj.items() if k != '_'
                ))
            elif isinstance(obj, str) or isinstance(obj, bytes):
                return repr(obj)
            elif hasattr(obj, '__iter__'):
                return '[{}]'.format(
                    ', '.join(TLObject.pretty_format(x) for x in obj)
                )
            else:
                return repr(obj)
        else:
            result = []
            if isinstance(obj, TLObject):
                obj = obj.to_dict()

            if isinstance(obj, dict):
                result.append(obj.get('_', 'dict'))
                result.append('(')
                if obj:
                    result.append('\n')
                    indent += 1
                    for k, v in obj.items():
                        if k == '_':
                            continue
                        result.append('\t' * indent)
                        result.append(k)
                        result.append('=')
                        result.append(TLObject.pretty_format(v, indent))
                        result.append(',\n')
                    result.pop()  # last ',\n'
                    indent -= 1
                    result.append('\n')
                    result.append('\t' * indent)
                result.append(')')

            elif isinstance(obj, str) or isinstance(obj, bytes):
                result.append(repr(obj))

            elif hasattr(obj, '__iter__'):
                result.append('[\n')
                indent += 1
                for x in obj:
                    result.append('\t' * indent)
                    result.append(TLObject.pretty_format(x, indent))
                    result.append(',\n')
                indent -= 1
                result.append('\t' * indent)
                result.append(']')

            else:
                result.append(repr(obj))

            return ''.join(result)

    @staticmethod
    def serialize_bytes(data):
        if not isinstance(data, bytes):
            if isinstance(data, str):
                data = data.encode('utf-8')
            else:
                raise TypeError(
                    'bytes or str expected, not {}'.format(type(data)))

        r = []
        if len(data) < 254:
            padding = (len(data) + 1) % 4
            if padding != 0:
                padding = 4 - padding

            r.append(bytes([len(data)]))
            r.append(data)

        else:
            padding = len(data) % 4
            if padding != 0:
                padding = 4 - padding

            r.append(bytes([
                254,
                len(data) % 256,
                (len(data) >> 8) % 256,
                (len(data) >> 16) % 256
            ]))
            r.append(data)

        r.append(bytes(padding))
        return b''.join(r)

    @staticmethod
    def serialize_datetime(dt):
        if not dt and not isinstance(dt, timedelta):
            return b'\0\0\0\0'

        if isinstance(dt, datetime):
            dt = _datetime_to_timestamp(dt)
        elif isinstance(dt, date):
            dt = _datetime_to_timestamp(datetime(dt.year, dt.month, dt.day))
        elif isinstance(dt, float):
            dt = int(dt)
        elif isinstance(dt, timedelta):
            dt = _datetime_to_timestamp(datetime.utcnow() + dt)

        if isinstance(dt, int):
            return struct.pack('<i', dt)

        raise TypeError('Cannot interpret "{}" as a date.'.format(dt))

    def __eq__(self, o):
        return isinstance(o, type(self)) and self.to_dict() == o.to_dict()

    def __ne__(self, o):
        return not isinstance(o, type(self)) or self.to_dict() != o.to_dict()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)

    def to_dict(self):
        raise NotImplementedError

    def to_json(self, fp=None, default=_json_default, **kwargs):
        d = self.to_dict()
        if fp:
            return json.dump(d, fp, default=default, **kwargs)
        else:
            return json.dumps(d, default=default, **kwargs)

    def __bytes__(self):
        try:
            return self._bytes()
        except AttributeError:
            raise TypeError('a TLObject was expected but found something else')
    def _bytes(self):
        raise NotImplementedError

    @classmethod
    def from_reader(cls, reader):
        raise NotImplementedError

class MessageEmpty(TLObject):
    CONSTRUCTOR_ID = 0x90a6ca84
    SUBCLASS_OF_ID = 0x790009e3

    def __init__(self, id: int, peer_id: typing.Optional['TypePeer']=None):
        self.id = id
        self.peer_id = peer_id

    def to_dict(self):
        return {
            '_': 'MessageEmpty',
            'id': self.id,
            'peer_id': self.peer_id.to_dict() if isinstance(self.peer_id, TLObject) else self.peer_id
        }

    def _bytes(self):
        return b''.join((
            b'\x84\xca\xa6\x90',
            struct.pack('<I', (0 if self.peer_id is None or self.peer_id is False else 1)),
            struct.pack('<i', self.id),
            b'' if self.peer_id is None or self.peer_id is False else (self.peer_id._bytes()),
        ))

    @classmethod
    def from_reader(cls, reader):
        flags = reader.read_int()

        _id = reader.read_int()
        if flags & 1:
            _peer_id = reader.tgread_object()
        else:
            _peer_id = None
        return cls(id=_id, peer_id=_peer_id)

class MessageEntityBankCard(TLObject):
    CONSTRUCTOR_ID = 0x761e6af4
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityBankCard',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\xf4j\x1ev',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityBold(TLObject):
    CONSTRUCTOR_ID = 0xbd610bc9
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityBold',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\xc9\x0ba\xbd',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityCode(TLObject):
    CONSTRUCTOR_ID = 0x28a20571
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityCode',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'q\x05\xa2(',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityHashtag(TLObject):
    CONSTRUCTOR_ID = 0x6f635b0d
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityHashtag',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\r[co',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityItalic(TLObject):
    CONSTRUCTOR_ID = 0x826f8b60
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityItalic',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'`\x8bo\x82',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityMention(TLObject):
    CONSTRUCTOR_ID = 0xfa04579d
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityMention',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\x9dW\x04\xfa',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityMentionName(TLObject):
    CONSTRUCTOR_ID = 0xdc7b1140
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int, user_id):
        self.offset = offset
        self.length = length
        self.user_id = user_id

    def to_dict(self):
        return {
            '_': 'MessageEntityMentionName',
            'offset': self.offset,
            'length': self.length,
            'user_id': self.user_id
        }

    def _bytes(self):
        return b''.join((
            b'@\x11{\xdc',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            struct.pack('<q', self.user_id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _user_id = reader.read_long()
        return cls(offset=_offset, length=_length, user_id=_user_id)

class MessageEntityPre(TLObject):
    CONSTRUCTOR_ID = 0x73924be0
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int, language: str):
        self.offset = offset
        self.length = length
        self.language = language

    def to_dict(self):
        return {
            '_': 'MessageEntityPre',
            'offset': self.offset,
            'length': self.length,
            'language': self.language
        }

    def _bytes(self):
        return b''.join((
            b'\xe0K\x92s',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            self.serialize_bytes(self.language),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _language = reader.tgread_string()
        return cls(offset=_offset, length=_length, language=_language)

class MessageEntityStrike(TLObject):
    CONSTRUCTOR_ID = 0xbf0693d4
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityStrike',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\xd4\x93\x06\xbf',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityTextUrl(TLObject):
    CONSTRUCTOR_ID = 0x76a6d327
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int, url: str):
        self.offset = offset
        self.length = length
        self.url = url

    def to_dict(self):
        return {
            '_': 'MessageEntityTextUrl',
            'offset': self.offset,
            'length': self.length,
            'url': self.url
        }

    def _bytes(self):
        return b''.join((
            b"'\xd3\xa6v",
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
            self.serialize_bytes(self.url),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        _url = reader.tgread_string()
        return cls(offset=_offset, length=_length, url=_url)

class MessageEntityUnderline(TLObject):
    CONSTRUCTOR_ID = 0x9c4e7e8b
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUnderline',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\x8b~N\x9c',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityUnknown(TLObject):
    CONSTRUCTOR_ID = 0xbb92ba95
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUnknown',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'\x95\xba\x92\xbb',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

class MessageEntityUrl(TLObject):
    CONSTRUCTOR_ID = 0x6ed02538
    SUBCLASS_OF_ID = 0xcf6419dc

    def __init__(self, offset: int, length: int):
        self.offset = offset
        self.length = length

    def to_dict(self):
        return {
            '_': 'MessageEntityUrl',
            'offset': self.offset,
            'length': self.length
        }

    def _bytes(self):
        return b''.join((
            b'8%\xd0n',
            struct.pack('<i', self.offset),
            struct.pack('<i', self.length),
        ))

    @classmethod
    def from_reader(cls, reader):
        _offset = reader.read_int()
        _length = reader.read_int()
        return cls(offset=_offset, length=_length)

    def _bytes(self):
        return b''.join((
            b'[\x1bf\xab',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()

DEFAULT_URL_RE = compile(r'\[([\S\s]+?)\]\((.+?)\)')
DEFAULT_URL_FORMAT = '[{0}]({1})'
DEFAULT_DELIMITERS = {
    '**': MessageEntityBold,
    '__': MessageEntityItalic,
    '~~': MessageEntityStrike,
    '``': MessageEntityCode,
    '```': MessageEntityPre,
    '@': MessageEntityMention,
    '#': MessageEntityHashtag,
    '_': MessageEntityUnderline,
}

class MarkDown(object):

    def __init__(self, *args) -> (None):
        pass

    def add_surrogate(self, text):
        return ''.join(
            ''.join(chr(y) for y in struct.unpack('<HH', x.encode('utf-16le')))
            if (0x10000 <= ord(x) <= 0x10FFFF) else x for x in text
        )

    def del_surrogate(self, text):
        return text.encode('utf-16', 'surrogatepass').decode('utf-16')

    def strip_text(self, text, entities):
        if not entities:
            return text.strip()

        while text and text[-1].isspace():
            e = entities[-1]
            if e.offset + e.length == len(text):
                if e.length == 1:
                    del entities[-1]
                    if not entities:
                        return text.strip()
                else:
                    e.length -= 1
            text = text[:-1]

        while text and text[0].isspace():
            for i in reversed(range(len(entities))):
                e = entities[i]
                if e.offset != 0:
                    e.offset -= 1
                    continue

                if e.length == 1:
                    del entities[0]
                    if not entities:
                        return text.lstrip()
                else:
                    e.length -= 1

            text = text[1:]

        return text

    def parse(self, message, delimiters=None, url_re=None):
        if not message:
            return message, []

        if url_re is None:
            url_re = DEFAULT_URL_RE
        elif isinstance(url_re, str):
            url_re = compile(url_re)

        if not delimiters:
            if delimiters is not None:
                return message, []
            delimiters = DEFAULT_DELIMITERS

        delim_re = compile('|'.join('({})'.format(escape(k))
                                for k in sorted(delimiters, key=len, reverse=True)))
        i = 0
        result = []
        message = self.add_surrogate(message)
        while i < len(message):
            m = delim_re.match(message, pos=i)
            if m:
                delim = next(filter(None, m.groups()))
                end = message.find(delim, i + len(delim) + 1)
                if end != -1:
                    message = ''.join((
                            message[:i],
                            message[i + len(delim):end],
                            message[end + len(delim):]
                    ))
                    for ent in result:
                        if ent.offset + ent.length > i:
                            if ent.offset <= i:
                                ent.length -= len(delim) * 2
                            else:
                                ent.length -= len(delim)
                    ent = delimiters[delim]
                    if ent == MessageEntityPre:
                        result.append(ent(i, end - i - len(delim), ''))  # has 'lang'
                    else:
                        result.append(ent(i, end - i - len(delim)))

                    if ent in (MessageEntityCode, MessageEntityPre):
                        i = end - len(delim)

                    continue

            elif url_re:
                m = url_re.match(message, pos=i)
                if m:
                    message = ''.join((
                        message[:m.start()],
                        m.group(1),
                        message[m.end():]
                    ))

                    delim_size = m.end() - m.start() - len(m.group())
                    for ent in result:
                        if ent.offset + ent.length > m.start():
                            ent.length -= delim_size

                    result.append(MessageEntityTextUrl(
                        offset=m.start(), length=len(m.group(1)),
                        url=del_surrogate(m.group(2))
                    ))
                    i += len(m.group(1))
                    continue

            i += 1

        message = self.strip_text(message, result)
        return self.del_surrogate(message), result

class Metas(object):
    
    def __init__(self, text: str, user_ids, action: bool = True, *args) -> (None):
        self.text, self.user_ids, self.action = text, user_ids, action

    def __replacer(self, text: str, action: bool = 'regex', mode: bool = True) -> (str):

        if action == 'regex':
            for word in (compile(r'\_\_'), compile(r'\*\*'), compile(r'\`\`')):
                text: str = sub(word, '', text)
            else:
                return text

        elif action == 'replace':
            
            #text: str = text.replace('____', '')
            plorer, index_list = search(r'(\@.*?\_\_\w+\_\_\w+)|(\@.*?\_\_\_\_\w+)', text), []

            if mode:
                text: list = [*text]
                for i, n in zip(text, range(len(text))):
                    try:
                        if i == '_' and text[n+1 if not len(text) == n + 1 else n-1] != '_' and text[n-1 if n != 0 else n+1] != '_':
                            index_list.append(n)
                            text[n] = ''
                    except IndexError:
                        pass
                else:
                    text: str = ''.join(text)

            if plorer:

                finds, main_index_list, texts = findall(r'(\@.*?\_\_\w+\_\_\w+)|(\@.*?\_\_\_\_\w+)', text), [], text

                for find in finds:
                    if isinstance(find, tuple) or isinstance(find, list):
                        find: str = ''.join(list(find))
                        if find == '':
                            break
                    for word in ('__', '``', '**'):
                        if [*texts].count(word[0]) >= 4:
                            if str([*texts].count(word[0]) / 4).split('.')[1] == '0':
                                texts: str = texts.replace(word, '')
                            else:
                                texts: str = texts.replace(word, '', int([*texts].count(word[0]) / 2) - 1)
                    else:
                        main_index_list.append(texts.find(find.replace('__', '')))
                    text: str = text.replace(find, '', 1)

            for word in ('__', '**', '``'):
                if [*text].count(word[0]) >= 4:
                    if str([*text].count(word[0]) / 4).split('.')[1] == '0':
                        text: str = text.replace(word, '')
                    else:
                        text: str = text.replace(word, '', int([*text].count(word[0]) / 2) - 1)
            else:

                if plorer:

                    texts: list = [*text]

                    for index, find, num in zip(main_index_list, finds, range(len(finds))):
                        if isinstance(find, tuple) or isinstance(find, list):
                            find: str = ''.join(list(find))
                        texts.insert(index, find)
                    if mode:
                        list(map(lambda number: texts.insert(number, '_'), index_list)) # int(len(findall(r'\_', text)) ** 2)
                    
                    return ''.join(texts)
                else:
                    return text

        else:
            return text.replace('**', '', len(findall(r'\*\*(.*?)\*\*', text)) + 1).replace('__', '', len(findall(r'(\_\_(.*?)\_\_)', text)) + 1).replace('``', '', len(findall(r'\`\`(.*?)\`\`', text)) + 1)

    def replacer(self, text: str, action: str = 'replace'):
        return self.__replacer(text, action)

    def __to_parse(self, text: str, user_ids: list = None, filter_hashtag: bool = True, filter_under_line: bool = True) -> (tuple):

        if not filter_hashtag:
            DEFAULT_DELIMITERS.pop('#')
        if not filter_under_line:
            DEFAULT_DELIMITERS.pop('_')

        mark, params, action, count = MarkDown(), [], '', 0

        for text in (mark.parse(text)):

            if isinstance(text, str):
                real_text: str = text

            else:

                for clean in text:

                    if isinstance(clean, MessageEntityBold):
                        action: str = 'Bold'
                    elif isinstance(clean, MessageEntityItalic):
                        action: str = 'Italic'
                    elif isinstance(clean, MessageEntityStrike):
                        action: str = 'Strike'
                    elif isinstance(clean, MessageEntityCode) or isinstance(clean, MessageEntityPre):
                        action: str = 'Mono'
                    elif isinstance(clean, MessageEntityMention):
                        action: str = 'MentionText'
                    
                    if not isinstance(clean, MessageEntityMention):
                        params.extend([{'from_index': clean.offset, 'length': clean.length, 'type': action}])
                    
                    else:
                        guid: str = user_ids[count]
                        params.extend([{'type': action, 'mention_text_object_guid': guid, 'from_index': clean.offset, 'length': clean.length, 'mention_text_object_type': 'User'}])
                        count: int = count.__add__(1)
                
                else:
                    return params, real_text

    @property
    def checker(self) -> (list):
        
        if self.user_ids or self.action:
            return self.__to_parse(self.text, self.user_ids, False, False)
        else:
            result, texts = [], self.__replacer(self.text, action='replace')

            if ('**' in self.text):
                
                Bold: list = findall(r'\*\*(.*?)\*\*', self.text)
                boldFromIndex: list = [self.text.index(i) for i in Bold]
                [(result.append({'from_index': from_index, 'length': len(length), 'type': 'Bold'})) for from_index, length in zip(boldFromIndex, Bold)]
            
            if ('__' in self.text):
                
                Italic: list = findall(r'\_\_(.*?)\_\_', self.text)
                ItalicFromIndex: list = [self.text.index(i) for i in Italic]
                [(result.append({'from_index': from_index, 'length': len(length), 'type': 'Italic'})) for from_index, length in zip(ItalicFromIndex, Italic)]
            
            if ('``' in self.text):
                
                Mono: list = findall(r'\`\`(.*?)\`\`', self.text)
                monoFromIndex: list = [self.text.index(i) for i in Mono]
                [self.text.index(i) for i in Mono]
                [(result.append({'from_index': from_index, 'length': len(length), 'type': 'Mono'})) for from_index, length in zip(monoFromIndex, Mono)]
            
            return result, texts

class Tags(object):
    
    def __init__(self, text: str, *args) -> (dict):
        self.text: str = text

    def __replacer(self, text: str) -> (str):
        return sub(compile(r'\@'), '', text)

    def checker(
        self,
        guids: list =   None,
        types: list =   None
        ) -> (tuple):
        
        if ('@' in self.text and [*str(self.text)].count('@') >= 2):

            Tags: list = findall(r'\@(\w+)\@', self.text)

            # TODO: set object type
            return [{'type': 'MentionText', 'mention_text_object_guid': guid, 'from_index': from_index, 'length': len(length), 'mention_text_object_type': 'User'} for from_index, length, guid in zip(list(map(lambda i: self.text.index(i), Tags)), Tags, guids)], self.__replacer(self.text)

from html import escape # html escape 

def _add_surrogate(text):
    return ''.join(
        ''.join(chr(y) for y in struct.unpack('<HH', x.encode('utf-16le')))
        if (0x10000 <= ord(x) <= 0x10FFFF) else x for x in text
    )

def _del_surrogate(text):
    return text.encode('utf-16', 'surrogatepass').decode('utf-16')

class TypeMessageEntity(object):
    pass

class HTMLToTelegramParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ''
        self.entities = []
        self._building_entities = {}
        self._open_tags = deque()
        self._open_tags_meta = deque()

    def handle_starttag(self, tag, attrs):
        self._open_tags.appendleft(tag)
        self._open_tags_meta.appendleft(None)

        attrs = dict(attrs)
        EntityType = None
        args = {}
        if tag == 'strong' or tag == 'b':
            EntityType = MessageEntityBold
        elif tag == 'em' or tag == 'i':
            EntityType = MessageEntityItalic
        elif tag == 'u':
            EntityType = MessageEntityUnderline
        elif tag == 'del' or tag == 's':
            EntityType = MessageEntityStrike
        elif tag == 'blockquote':
            EntityType = MessageEntityBlockquote
        elif tag == 'code':
            try:
                pre = self._building_entities['pre']
                try:
                    pre.language = attrs['class'][len('language-'):]
                except KeyError:
                    pass
            except KeyError:
                EntityType = MessageEntityCode
        elif tag == 'pre':
            EntityType = MessageEntityPre
            args['language'] = ''
        elif tag == 'a':
            try:
                url = attrs['href']
            except KeyError:
                return
            if url.startswith('mailto:'):
                url = url[len('mailto:'):]
                EntityType = MessageEntityEmail
            else:
                if self.get_starttag_text() == url:
                    EntityType = MessageEntityUrl
                else:
                    EntityType = MessageEntityTextUrl
                    args['url'] = _del_surrogate(url)
                    url = None
            self._open_tags_meta.popleft()
            self._open_tags_meta.appendleft(url)

        if EntityType and tag not in self._building_entities:
            self._building_entities[tag] = EntityType(
                offset=len(self.text),
                length=0,
                **args)

    def handle_data(self, text):
        previous_tag = self._open_tags[0] if len(self._open_tags) > 0 else ''
        if previous_tag == 'a':
            url = self._open_tags_meta[0]
            if url:
                text = url

        for tag, entity in self._building_entities.items():
            entity.length += len(text)

        self.text += text

    def handle_endtag(self, tag):
        try:
            self._open_tags.popleft()
            self._open_tags_meta.popleft()
        except IndexError:
            pass
        entity = self._building_entities.pop(tag, None)
        if entity:
            self.entities.append(entity)

def parse(html: str) -> typing.Tuple[str, typing.List[TypeMessageEntity]]:
    if not html:
        return html, []

    parser = HTMLToTelegramParser()
    parser.feed(_add_surrogate(html))
    text = helpers.strip_text(parser.text, parser.entities)
    return _del_surrogate(text), parser.entities

def unparse(text: str, entities: typing.Iterable[TypeMessageEntity], _offset: int = 0,
            _length: typing.Optional[int] = None) -> str:

    if not text:
        return text
    elif not entities:
        return escape(text)

    text = _add_surrogate(text)
    if _length is None:
        _length = len(text)
    html = []
    last_offset = 0
    for i, entity in enumerate(entities):
        if entity.offset >= _offset + _length:
            break
        relative_offset = entity.offset - _offset
        if relative_offset > last_offset:
            html.append(escape(text[last_offset:relative_offset]))
        elif relative_offset < last_offset:
            continue

        skip_entity = False
        length = entity.length

        while helpers.within_surrogate(text, relative_offset, length=_length):
            relative_offset += 1

        while helpers.within_surrogate(text, relative_offset + length, length=_length):
            length += 1

        entity_text = unparse(text=text[relative_offset:relative_offset + length],
                              entities=entities[i + 1:],
                              _offset=entity.offset, _length=length)
        entity_type = type(entity)

        if entity_type == MessageEntityBold:
            html.append('<strong>{}</strong>'.format(entity_text))
        elif entity_type == MessageEntityItalic:
            html.append('<em>{}</em>'.format(entity_text))
        elif entity_type == MessageEntityCode:
            html.append('<code>{}</code>'.format(entity_text))
        elif entity_type == MessageEntityUnderline:
            html.append('<u>{}</u>'.format(entity_text))
        elif entity_type == MessageEntityStrike:
            html.append('<del>{}</del>'.format(entity_text))
        elif entity_type == MessageEntityBlockquote:
            html.append('<blockquote>{}</blockquote>'.format(entity_text))
        elif entity_type == MessageEntityPre:
            if entity.language:
                html.append(
                    "<pre>\n"
                    "    <code class='language-{}'>\n"
                    "        {}\n"
                    "    </code>\n"
                    "</pre>".format(entity.language, entity_text))
            else:
                html.append('<pre><code>{}</code></pre>'
                            .format(entity_text))
        elif entity_type == MessageEntityEmail:
            html.append('<a href="mailto:{0}">{0}</a>'.format(entity_text))
        elif entity_type == MessageEntityUrl:
            html.append('<a href="{0}">{0}</a>'.format(entity_text))
        elif entity_type == MessageEntityTextUrl:
            html.append('<a href="{}">{}</a>'
                        .format(escape(entity.url), entity_text))
        elif entity_type == MessageEntityMentionName:
            html.append('<a href="tg://user?id={}">{}</a>'
                        .format(entity.user_id, entity_text))
        else:
            skip_entity = True
        last_offset = relative_offset + (0 if skip_entity else length)

    while helpers.within_surrogate(text, last_offset, length=_length):
        last_offset += 1

    html.append(escape(text[last_offset:]))
    return _del_surrogate(''.join(html))

class MetaDataLoader(object):
    
    @classmethod
    def __init__(cls, caption: str,
                 metadata: dict = None) -> (None):
        cls.text, cls.meta = caption, metadata
    
    def __max(cls) -> (dict):
        pass