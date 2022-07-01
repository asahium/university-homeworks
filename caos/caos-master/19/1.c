#include <stdio.h>
#include <signal.h>
#include <unistd.h>

volatile int counter = 0;

void handler(int _) {
    (void)_;

    if (counter == 4)
        _exit(0);

    printf("%d\n", counter++);
    fflush(stdout);
}

int main() {
    struct sigaction action = {};
    action.sa_flags = SA_RESTART;
    action.sa_handler = handler;

    sigaction(SIGINT, &action, NULL);

    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, SIGINT);

    sigprocmask(SIG_BLOCK, &set, NULL);

    printf("%d\n", getpid());
    fflush(stdout);

    sigprocmask(SIG_UNBLOCK, &set, NULL);

    while (1)
        pause();
}
