#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdint.h>

volatile int counter = 0;
volatile int mode = 0;

void handler(int _) {
    if (_ == SIGUSR1) {
        ++counter;

        if (mode == 0)
            mode = 1;
        else
            mode = 0;
    }

    if (counter == 5)
        _exit(0);

    if (_ == SIGUSR2) {
        unsigned int n;

        scanf("%o", &n);

        if ((!(n & (1 << 31))) || (n & (1 << 30))) {
            printf("0\n");
            fflush(stdout);
            return;
        }

        n <<= 1;
        n >>= 1;

        if (!mode)
            n >>= 16;
        else
            n &= (1 << 16) - 1;

        printf("%d\n", n);
        fflush(stdout);
    }
}

int main() {
    struct sigaction action = {};
    action.sa_flags = SA_RESTART;
    action.sa_handler = handler;

    sigaction(SIGUSR2, &action, NULL);
    sigaction(SIGUSR1, &action, NULL);

    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, SIGUSR2);
    sigaddset(&set, SIGUSR1);

    sigprocmask(SIG_BLOCK, &set, NULL);

    printf("%d\n", getpid());
    fflush(stdout);

    sigprocmask(SIG_UNBLOCK, &set, NULL);

    while (1)
        pause();
}
