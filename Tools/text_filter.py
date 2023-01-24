#!/bin/python

import re, typing

DEFAULT_INAPPROPRIATE_WORDS = ['bad', 'evil',
                               'horrible', 'awful',
                               'fuck', 'bitch', 'unlike']

def detecting(__text: str, __inappropriate_words: list = None,
              __replace_to_char: typing.Union[str, list] = '-*~',
              action: bool = False) -> tuple:
    
    '''
    # a filter detection and text cleaner
    
    `text`: main text
    `inappropriate_words`: filter words: open('filter_words.sty','r').read().splitlines()
    `action`: replace to char: True = b-a-d, False = --- 
    
    '''
    
    if not __inappropriate_words:
        __inappropriate_words: list = DEFAULT_INAPPROPRIATE_WORDS
        
    search, replace_to_char = False,  __import__('random').choice(__replace_to_char)
    
    for word in __inappropriate_words: 
        find = re.compile(word).search(__text, re.IGNORECASE)
        if find:
            __text, search = re.sub(re.compile(__text[find.span()[0]:find.span()[1]]), ''.join(list(map(lambda i: replace_to_char, range(len(word))))) if not action else replace_to_char.join([*word]), __text, 1), True
    else:
        return search, __text

print(detecting('this is a bad day and and unlike this day'))
