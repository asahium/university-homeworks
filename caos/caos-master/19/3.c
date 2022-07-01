#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile int mode = 0;

void handler(int signal) {
    if (signal == SIGUSR1)
        mode = 1;
    else if (signal == SIGUSR2)
        mode = 2;
    else if (signal == SIGTERM)
        mode = -1;
}

int main() {
    struct sigaction action = {};
    action.sa_flags = SA_RESTART;
    action.sa_handler = handler;

    sigaction(SIGUSR1, &action, NULL);
    sigaction(SIGUSR2, &action, NULL);
    sigaction(SIGTERM, &action, NULL);

    sigset_t current;
    sigset_t last;

    sigemptyset(&current);

    sigaddset(&current, SIGUSR1);
    sigaddset(&current, SIGUSR2);
    sigaddset(&current, SIGTERM);

    sigprocmask(SIG_BLOCK, &current, &last);

    printf("%d\n", getpid());
    fflush(stdout);

    int one = 0, two = 0;

    while (1) {
        while (!mode)
            sigsuspend(&last);

        if (mode == -1)
            _exit(0);

        if (mode == 2) {
            ++two;
        } else {
            printf("%d %d\n", one, two);
            fflush(stdout);
            ++one;
        }

        mode = 0;
    }
}
