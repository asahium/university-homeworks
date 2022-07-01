#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdint.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdlib.h>
#include <errno.h>

volatile int mode = 0;

void handler(int signal) {
    if (signal == SIGTERM)
        mode = -1;
    else if (signal >= SIGRTMIN && signal <= SIGRTMAX)
        mode = signal - SIGRTMIN + 1;
}

int main(int count, char ** argv) {
    --count;

    int f_status[count];
    int f_descriptors[count];
    int64_t f_read[count];

    for (int j = 0; j < count; ++j) {
        f_status[j] = 0;
        f_read[j] = 0;
        f_descriptors[j] = open(argv[1 + j], O_RDONLY, 0400);
    }

    struct sigaction action = {};
    action.sa_flags = 0;
    action.sa_handler = handler;

    sigaction(SIGTERM, &action, NULL);

    for (int i = 0; i < count; ++i)
        sigaction(SIGRTMIN + i, &action, NULL);

    sigset_t current;
    sigset_t last;

    sigemptyset(&current);
    sigaddset(&current, SIGTERM);

    for (int i = 0; i < count; ++i)
        sigaddset(&current, SIGRTMIN + i);

    sigprocmask(SIG_BLOCK, &current, &last);

    printf("%d\n", getpid());
    fflush(stdout);

    while (1) {
        while (!mode)
            sigsuspend(&last);

        if (mode == -1) {
            for (int i = 0; i < count; ++i) {
                printf("%" PRId64 "\n", f_read[i]);

                if (!f_status[i])
                    close(f_descriptors[i]);
            }

            fflush(stdout);

            _exit(0);
        }

        int f_id = mode - 1;

        if (f_status[f_id]) {
            mode = 0;
            continue;
        }

        char buf[16];

        errno = 0;

        sigprocmask(SIG_UNBLOCK, &current, &last);

        int res = read(f_descriptors[f_id], buf, 16);

        sigprocmask(SIG_BLOCK, &current, &last);

        if (errno == EINTR)
            continue;

        if (res == 16)
            f_read[f_id] += strtoll(buf, NULL, 0);
        else {
            close(f_descriptors[f_id]);
            f_status[f_id] = 1;
            mode = 0;
        }
    }
}
