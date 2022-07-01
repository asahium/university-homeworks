/*Взято с семинара 194 группы*/
#include <stdio.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>


void sig_handler(int _) {
    _exit(0);
}

int main(int argc, char** argv) {
    char * host = argv[1];
    char * service = argv[2];
    char * key = argv[3];
    struct sigaction sa;
    sa.sa_handler = sig_handler;
    sigaction(SIGPIPE, &sa, NULL);
    struct addrinfo hints = {};
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    struct addrinfo *res = NULL;
    int err = getaddrinfo(host, service, &hints, &res);
    if (err) {
        fprintf(stderr, "%s\n", gai_strerror(err));
        return 1;
    }
    int sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return 1;
    }
    int val = 1;
    setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
    setsockopt(sock, SOL_SOCKET, SO_REUSEPORT, &val, sizeof(val));
    if (connect(sock, res->ai_addr, res->ai_addrlen) < 0) {
        return 1;
    }
    FILE* socket_pipe_read = fdopen(sock, "r");
    FILE* socket_pipe_write = fdopen(dup(sock), "w");
    fprintf(socket_pipe_write, "%s\n", key);
    if (fflush(socket_pipe_write) < 0) {
        return 0;
    }
    unsigned int k;
    if (fscanf(socket_pipe_read, "%u", &k) != 1) {
        return 0;
    }
    for (unsigned i = 0; i <= k; ++i) {
        fprintf(socket_pipe_write, "%d\n", i);
        if (ferror(socket_pipe_write)) {
            return 0;
        }

    }
    if (fflush(socket_pipe_write) < 0) {
        return 0;
    }
    unsigned long long answer;
    if (fscanf(socket_pipe_read, "%llu", &answer) != 1) {
        return 0;
    }
    printf("%llu\n", answer);
    fclose(socket_pipe_read);
    fclose(socket_pipe_write);
}