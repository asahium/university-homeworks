#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile int mode = 0;

void handler(int signal) {
    if (signal == SIGUSR1)
        mode = 0;
    else if (signal == SIGUSR2)
        mode = 1;
}

int main() {
    struct sigaction action = {};
    action.sa_flags = SA_RESTART;
    action.sa_handler = handler;

    sigaction(SIGUSR1, &action, NULL);
    sigaction(SIGUSR2, &action, NULL);

    printf("%d\n", getpid());
    fflush(stdout);

    int res;

    while (scanf("%d", &res) == 1) {
        printf("%d\n", mode ? res * res : -res);
        fflush(stdout);
    }
}
