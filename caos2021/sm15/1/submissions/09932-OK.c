#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void) {
    struct addrinfo hints = {};
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    char *host = NULL;
    char *service = NULL;
    struct addrinfo *result = NULL;
    while (scanf("%ms %ms", &host, &service) == 2) {
        result = NULL;
        int err = getaddrinfo(host, service, &hints, &result);
        if (err) {
            printf("%s\n", gai_strerror(err));
            free(host);
            free(service);
            freeaddrinfo(result);
        } else {
            struct sockaddr_in *min_sockaddr = (struct sockaddr_in *) result->ai_addr;
            struct addrinfo *result_iter = result;
            while (result_iter->ai_next) {
                result_iter = result_iter->ai_next;
                struct sockaddr_in *ain = (struct sockaddr_in *) result_iter->ai_addr;
                if (ntohl(ain->sin_addr.s_addr) < ntohl(min_sockaddr->sin_addr.s_addr)) {
                    min_sockaddr = ain;
                }
            }
            printf("%s:%d\n", inet_ntoa(min_sockaddr->sin_addr), ntohs(min_sockaddr->sin_port));
            free(host);
            free(service);
            freeaddrinfo(result);
        }
    }
    return 0;
}
