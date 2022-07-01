#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>

volatile double *sum;
volatile double *cur_s;
volatile double *cur_n;

void handler(int signo) {
    while (waitpid(-1, NULL, 0) > 0);
    printf("%.10g\n", *sum);
    fflush(stdout);
    exit(0);
}

int main(int argc, char **argv) {
    struct sigaction sa = {
            .sa_handler = handler,
            .sa_flags = SA_RESTART
    };
    sigemptyset(&sa.sa_mask);
    sigaction(SIGTERM, &sa, NULL);

    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd < 0) {
        _exit(0);
    }
    struct sockaddr_in ain = {
            .sin_family = AF_INET,
            .sin_port = htons(atoi(argv[1])),
            .sin_addr.s_addr = INADDR_ANY
    };
    int val = 1;

    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
    setsockopt(sfd, SOL_SOCKET, SO_REUSEPORT, &val, sizeof(val));

    if (bind(sfd, (void*)&ain, sizeof(ain)) < 0) {
        _exit(0);
    }

    if (listen(sfd, 5) < 0) {
        _exit(0);
    }


    sum = mmap(NULL, sizeof(double) * 2 + sizeof(int), PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANON, -1, 0);
    *sum = 0;

    cur_s = sum + sizeof(double);
    cur_n = cur_s + sizeof(int);

    while (1) {
        while (waitpid(-1, NULL, WNOHANG) > 0);

        struct sockaddr_in sa;
        socklen_t slen = sizeof(sa);

        int afd = accept(sfd, (void*) &sa, (unsigned*)&slen);
        if (afd < 0) {
            _exit(0);
        }

        pid_t pid;

        if (!(pid = fork())) {
            int afd1 = dup(afd);
            float tmp;
            double input;
            *cur_s = 0;
            *cur_n = 0;
            while (1) {
                if (read(afd1, &tmp, sizeof(float)) != sizeof(float)) {
                    break;
                }
                input = tmp;
                *cur_s += input;
                ++*cur_n;
            }
            close(afd);
            _exit(0);
        }

        if (*cur_n) {
            *sum += *cur_s / *cur_n;
        }

        close(afd);
    }
}