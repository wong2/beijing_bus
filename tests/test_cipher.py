#-*-coding:utf-8-*-

import unittest

from beijing_bus.cipher import Cipher


class CipherTest(unittest.TestCase):

    def test_encrypt(self):
        cipher = Cipher('aibang127')
        self.assertEqual(cipher.encrypt('运通122'), 'N+j17kGHx8Mj')
    
    def test_decrypt(self):
        cipher = Cipher('aibang127')
        self.assertEqual(cipher.decrypt('N+j17kGHx8Mj'), '运通122')
