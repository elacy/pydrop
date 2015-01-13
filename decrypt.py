#!/usr/bin/python
from Crypto.Cipher import AES
import os
import cgi

class Key:
        def __init__(self,key,IV):
                self.key = key
                self.IV = IV

def initCipher(key):
        from Crypto.Cipher import AES
        return AES.new(key.key, AES.MODE_CBC,key.IV)

def dropFile(dropDir,key):
        crypt = initCipher(key)
        chunksize = 65536
        encryptedFile = open(dropDir + '/input','rb')
        decrytpedFile = open(dropDir + '/output','w')
        while 1:
                data = encryptedFile.read(chunksize)
                if not data: break
                decrytpedFile.write(crypt.decrypt(data))
        encryptedFile.close()
        decrytpedFile.close()


basePath = '/var/www/django/dead'
dropPath = '/var/www/django/dead/drop/TB5KHCsok2'

file = open(dropPath + '/decryptedKey','rb')
key = Key(file.read(32),file.read(16))
file = open(dropPath + '/output','rb')
form = cgi.FieldStorage(environ={'REQUEST_METHOD':'POST'}, fp=file)
print form[" filename"][0]
decrytpedFile = open(dropPath + '/one','w')
while 1:
        data = form[" filename"][0].value.read(65536)
        if not data: break
        decrytpedFile.write(data)
decrytpedFile.close()