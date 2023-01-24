#!/bin/python

from Crypto.Cipher.AES      import MODE_CBC, block_size, new
from Crypto.Util.Padding    import pad, unpad
from base64                 import b64encode, urlsafe_b64decode

class Encryption(object):
    
    @classmethod
    
    def __init__(cls, auth_key: str) -> ...:
        if len(str(auth_key)) != 32:
            raise IndexError('len your session key is not \'32\'')
        cls.auth_key, cls.iv = bytearray((''.join(list(map(lambda a: chr((a - ord('a') + 9) % 26 + ord('a')), (str(auth_key[16:24] + auth_key[:8] + auth_key[24:32] + auth_key[8:16]).encode('latin-1')))))), 'utf-8'), bytearray.fromhex(str('0' * len(auth_key)))

    def encrypt(cls, data: str) -> (str):
        return (b64encode(new(cls.auth_key, MODE_CBC, iv=cls.iv).encrypt(pad(data.encode('utf-8'), block_size))).decode('utf-8'))

    def decrypt(cls, data: str) -> (str):
        return (unpad(new(cls.auth_key, MODE_CBC, iv=cls.iv).decrypt(urlsafe_b64decode(data.encode('utf-8'))), block_size)).decode('utf-8')

