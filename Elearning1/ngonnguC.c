#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <unistd.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    int flag = 1;
    setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(int));
    int size = 65536;
    setsockopt(sock, SOL_SOCKET, SO_RCVBUF, &size, sizeof(int));
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, &size, sizeof(int));
    printf("TCP_NODELAY và buffer đã được cấu hình.\n");
    close(sock);
    return 0;
}