#!/bin/python

def anti_spam(texts: list) -> dict:
        
        '''
        anti_spam(['Hey', 'Love', 'Hey'])
        '''

        result: dict = {'is_spam': False, 'spam_index_list': []}
        
        for text, index in zip(texts, range(len(texts))):
            texts.remove(text)
            list(map(lambda text: result['spam_index_list'].append(index), texts))
        
        else:
            if len(result.get('spam_index_list')) >= 1:
                result.update({'is_spam': True})
            return __import__('json').dumps(
                result,
                indent=2,
                ensure_ascii=False,
                default=lambda value: str(value)
                )

        #list(map(lambda text: (indexs.extend(texts.index(text)), texts.remove(text)) if texts.count(text) > 2 else ..., texts))
