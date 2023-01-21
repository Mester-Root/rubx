#!/bin/python
# anti words text spam

from rb.parser import MarkDown, MessageEntityCode

def parser(text: str, *args):
  match, results = MarkDown(), []
  for mark in match.parse(text, {'unlike': MessageEntityCode, 'bad': MessageEntityCode, 'fuck': MessageEntityCode, 'bitch': MessageEntityCode}):
    if isinstance(mark, str):
      real: str = mark
    else: list(map(lambda clean: results.extend([clean.offset, clean.length])))
  else:
    return real, results
