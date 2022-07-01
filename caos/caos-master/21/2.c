#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

volatile unsigned int lst = 0;
volatile unsigned int count = 0;

void handler(int _) {
    (void) _;

    printf("%u\n", lst);
    fflush(stdout);

    if (++count == 8)
        exit(0);
}

int prime(unsigned int n) {
    if (n < 2)
        return 0;

    for (unsigned i = 2; i * i <= n; ++i)
        if (!(n % i))
            return 0;

    return 1;
}

int main() {
    unsigned int low;
    unsigned int high;

    scanf("%u %u", &low, &high);

    struct sigaction sa = {
            .sa_handler = handler,
            .sa_flags = SA_RESTART
    };

    sigemptyset(&sa.sa_mask);
    sigaction(SIGVTALRM, &sa, NULL);

    struct itimerval it = {};

    it.it_value.tv_sec = 0;
    it.it_interval.tv_sec = 0;

    it.it_value.tv_usec = 100000;
    it.it_interval.tv_usec = 100000;

    setitimer(ITIMER_VIRTUAL, &it, NULL);

    for (unsigned int i = low; i < high; ++i)
        lst = prime(i) ? i : lst;

    if (count != 8) {
        printf("-1\n");
        fflush(stdout);
    }
}