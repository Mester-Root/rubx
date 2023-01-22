#!/bin/python
# anti words text spam

from rb.parser import MarkDown, MessageEntityCode

def parser(text: str, echo: list = None, *args):
    match, results, __max = MarkDown(), [], {}
  
    if not echo:
        echo = {'unlike': MessageEntityCode, 'bad': MessageEntityCode, 'fuck': MessageEntityCode, 'bitch': MessageEntityCode}

    else:
        if isinstance(echo, str):
            echo: list = [echo]
        list(map(lambda i: __max.update({i: MessageEntityCode}), echo))

    for mark in match.parse(text, echo):
        if isinstance(mark, str):
            real: str = mark
        else:
            list(map(lambda clean: results.extend([clean.offset, clean.length])))
    else:
        return real, results

# TO USE
print(parser('Hey is day bad and you bad'))
