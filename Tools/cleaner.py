#!/bin/python

from re import compile, sub, IGNORECASE
from random import choice

class ProfanitiesFilter(object):
    def __init__(
        self,
        filterlist: list,
        ignore_case: bool = True,
        replacements: str = "$@%-?!",
        complete: bool = True,
        inside_words: bool = False
        ) -> (...):

        self.badwords, self.ignore_case, self.replacements, self.complete, self.inside_words = filterlist, ignore_case, replacements, complete, inside_words

    def _make_clean_word(
        self  : 'ProfanitiesFilter',
        length: int
        ) -> (str):
        
        return ''.join(list(map(lambda i: choice(self.replacements), range(length))))
    
    def __replacer(
        self : 'ProfanitiesFilter',
        match: str
        ) -> (str):
        value = match.group()
        if self.complete:
            return self._make_clean_word(len(value))
        else:
            return value[0]+self._make_clean_word(len(value)-2)+value[-1]
    
    def clean(
        self: 'ProfanitiesFilter',
        text: 'str'
        ) -> (list):

        regexp_insidewords: dict = {
            True: r'(%s)',
            False: r'\b(%s)\b',
            }
        regexp: str = (regexp_insidewords[self.inside_words] % '|'.join(self.badwords))
        r = compile(regexp, IGNORECASE if self.ignore_case else 0)
        return [r.sub(self.__replacer, text), bool(text in self.badwords)]

# to use

anti = ProfanitiesFilter(['bad', 'dick', 'unlike', 'unlove', 'fuck', 'swear'], replacements=['-', '*'], inside_words=True)

print(anti.clean('Hey! My Bro r u bad and me unlike you and swear for u fuck you'))
