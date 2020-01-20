#!/usr/bin/env python 

import base64
import sys

import simple_aes_cipher

if len(sys.argv) != 3:
   print("Usage: " + sys.argv[0] + " shellcode key")

shellcode = sys.argv[1].replace('\\x', '').decode('hex')

if len(shellcode) % 16 != 0:
   for i in range(16 - len(shellcode) % 16 - 1):
      shellcode += "\x90"
pass_phrase = sys.argv[2]

secret_key = simple_aes_cipher.generate_secret_key(pass_phrase)
cipher = simple_aes_cipher.AESCipher(secret_key)

encrypt_text = cipher.encrypt(shellcode)
encrypted_shellcode = ""
for elmt in bytearray(base64.b64decode(encrypt_text)):
   encrypted_shellcode += '\\x' 
   encrypted_shellcode += '%02x' % elmt

print(encrypted_shellcode)
