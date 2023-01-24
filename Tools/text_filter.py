#!/bin/python

import re

def detecting(__text: str, __inappropriate_words: list = ['bad', 'evil', 'horrible', 'awful', 'fuck', 'bitch', 'unlike']):
    search: bool = False
    for word in __inappropriate_words: 
        find = re.compile(word).search(__text, re.IGNORECASE)
        if find:
            __text, search = re.sub(re.compile(__text[find.span()[0]:find.span()[1]]), ''.join(list(map(lambda i: '-', range(len(word))))), __text, 1), True
    else:
        return search, __text

print(detecting('this is a bad day and and unlike this day'))
