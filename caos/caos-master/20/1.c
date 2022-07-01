#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <stdio.h>

int main() {
    char host[1000];
    char service[1000];

    struct addrinfo hints;
    struct addrinfo *result, *it;
    struct sockaddr_in * ipv4;
    struct sockaddr_in * min_ipv4 = NULL;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;

    while (scanf("%s %s", host, service) == 2) {
        int status = getaddrinfo(host, service, &hints, &result);

        if (status != 0) {
            printf("%s\n", gai_strerror(status));
            continue;
        }

        for (it = result; it != NULL; it = it->ai_next) {
            ipv4 = (struct sockaddr_in *)it->ai_addr;

            if (!min_ipv4) {
                min_ipv4 = ipv4;
                continue;
            }

            uint32_t cur = ntohl(ipv4->sin_addr.s_addr);
            uint32_t lst = ntohl(min_ipv4->sin_addr.s_addr);

            if (cur < lst)
                min_ipv4 = ipv4;
        }

        printf("%s:%d\n",
                inet_ntoa(min_ipv4->sin_addr),
                ntohs(min_ipv4->sin_port));

        freeaddrinfo(result);

        *host = '\0';
        *service = '\0';

        min_ipv4 = NULL;
    }
}