#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile int mode = 0;

void process(int signal) {
    if (signal == SIGTERM) {
        mode = -1;
    }
    else if (signal == SIGUSR1) {
        mode = 1;
    }
    else if (signal == SIGUSR2) {
        mode = 2;
    }
}

int main(void) {
    struct sigaction action = {};
    action.sa_flags = SA_RESTART;
    action.sa_handler = process;
    sigaction(SIGUSR1, &action, NULL);
    sigaction(SIGUSR2, &action, NULL);
    sigaction(SIGTERM, &action, NULL);
    sigset_t cur;
    sigset_t last;
    sigemptyset(&cur);
    sigaddset(&cur, SIGUSR1);
    sigaddset(&cur, SIGUSR2);
    sigaddset(&cur, SIGTERM);
    sigprocmask(SIG_BLOCK, &cur, &last);
    printf("%d\n", getpid());
    fflush(stdout);
    int a = 0, b = 0;

    while (1) {
        while (!mode) {
            sigsuspend(&last);
        }
        if (mode == -1) {
            _exit(0);
        }
        if (mode == 2) {
            ++b;
        } else {
            printf("%d %d\n", a, b);
            fflush(stdout);
            ++a;
        }
        mode = 0;
    }
}