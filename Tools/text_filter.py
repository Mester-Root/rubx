#!/bin/python

import re, typing

def detecting(__text: str, __inappropriate_words: list = ['bad', 'evil', 'horrible', 'awful', 'fuck', 'bitch', 'unlike'], __replace_to_char: typing.Union[str, list] = '-*~') -> tuple:
    search, replace_to_char = False,  __import__('random').choice(__replace_to_char)
    for word in __inappropriate_words: 
        find = re.compile(word).search(__text, re.IGNORECASE)
        if find:
            __text, search = re.sub(re.compile(__text[find.span()[0]:find.span()[1]]), ''.join(list(map(lambda i: replace_to_char, range(len(word))))), __text, 1), True
    else:
        return search, __text

print(detecting('this is a bad day and and unlike this day'))
