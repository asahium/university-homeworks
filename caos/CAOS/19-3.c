#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char **argv) {
    struct sockaddr_in addr = {
            .sin_family = AF_INET,
            .sin_port = htons(atoi(argv[1])),
            .sin_addr.s_addr = INADDR_ANY
    };
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) {
        _exit(0);
    }
    int val = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
    setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &val, sizeof(val));
    if (bind(fd, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
        _exit(0);
    }
    if (listen(fd, 5) < 0) {
        _exit(0);
    }
    int32_t res = 0;
    int32_t input = 1;
    while (input) {
        int size = sizeof(addr);
        int sfd = accept(fd, (struct sockaddr *) &addr, (socklen_t *) &size);
        if (sfd < 0) {
            _exit(0);
        }
        read(sfd, &input, sizeof(input));
        close(sfd);
        res += ntohl(input);
    }
    printf("%" PRId32 "\n", res);
    fflush(stdout);
    close(fd);
}