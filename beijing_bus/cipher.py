# -*-coding:utf-8-*-

"""

加密算法的实现 (实际上是RC4)

http://zh.wikipedia.org/wiki/RC4

>>> cipher = Cipher('aibang127')
>>> print cipher.decrypt('N+j17kGHx8Mj')
运通122

"""

import copy
import base64
import hashlib


class Cipher(object):

    def __init__(self, key):
        k = bytearray(self._md5(key))
        self.s_box = self._get_s_box(k)

    def _md5(self, data):
        return hashlib.md5(data).hexdigest()

    def _get_s_box(self, key):
        s_box = range(256)
        j = 0
        for i in range(256):
            j = (j + s_box[i] + key[i % len(key)]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
        return s_box

    def calc(self, data):
        s_box = copy.copy(self.s_box)
        results = range(len(data))
        j = 0
        for i in range(len(data)):
            k = (i + 1) % 256
            j = (j + s_box[k]) % 256
            s_box[j], s_box[k] = s_box[k], s_box[j]
            n = (s_box[j] + s_box[k]) % 256
            results[i] = data[i] ^ s_box[n]
        return results

    def decrypt(self, message, decode=base64.b64decode):
        message = decode(message)
        data = bytearray(message)
        return str(bytearray(self.calc(data)))

    def encrypt(self, message, encode=base64.b64encode):
        data = bytearray(message)
        message = str(bytearray(self.calc(data)))
        return encode(message)
