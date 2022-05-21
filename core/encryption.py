#!/usr/bin/python

from config import *
from Crypto.Cipher import AES
from Crypto.Random import new as Random
from base64 import b64encode,b64decode

class AESCipher:
  def __init__(self,data,key):
    self.block_size = 16
    self.data = data
    self.key = key
    self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
    self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

  def encrypt(self):
    plain_text = self.pad(self.data)
    iv = Random().read(AES.block_size)
    cipher = AES.new(self.key,AES.MODE_CBC,iv)
    return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()

  def decrypt(self):
    cipher_text = b64decode(self.data.encode())
    iv = cipher_text[:self.block_size]
    cipher = AES.new(self.key,AES.MODE_CBC,iv)
    return self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()

def encrypt(cmd):
    return AESCipher(cmd, key).encrypt()

def decrypt(data):
    return AESCipher(data, key).decrypt()