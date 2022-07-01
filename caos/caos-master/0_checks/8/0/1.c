#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <fcntl.h>

#include <unistd.h>

volatile int counter = 0;

void handler(int signo) {
    if (signo == SIGUSR1) {
        counter += 5;
    }
    if (signo == SIGUSR2) {
        counter -= 4;
    }
    printf("%d %d\n", signo, counter);
    fflush(stdout);
    if (counter < 0) {
        _exit(0);
    }
}


int main() {
    struct sigaction sa1 = {
            .sa_handler = handler,
            .sa_flags = SA_RESTART
    };

    sigemptyset(&sa1.sa_mask);
    sigaction(SIGUSR1, &sa1, NULL);
    sigaction(SIGUSR2, &sa1, NULL);

    printf("%d\n", getpid());
    fflush(stdout);
    while (1) {
        pause();
    }
}