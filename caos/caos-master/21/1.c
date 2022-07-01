#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

void handler(int _) {
    (void)_;
    exit(0);
}

int main() {
    struct sigaction sa = {
            .sa_handler = handler,
            .sa_flags = SA_RESTART
    };

    sigemptyset(&sa.sa_mask);
    sigaction(SIGALRM, &sa, NULL);

    time_t one;
    long two;

    scanf("%ld %ld", &one, &two);

    struct timeval now = {};
    gettimeofday(&now, NULL);

    long sec = one - now.tv_sec;
    long usec = two / 1000 - now.tv_usec;
    long timeout = 1000000 * sec + usec;

    if (timeout < 0)
        exit(0);

    struct itimerval till = {};
    till.it_value.tv_sec = timeout / 1000 / 1000;
    till.it_value.tv_usec = timeout % 1000000;

    setitimer(ITIMER_REAL, &till, NULL);
    pause();
}