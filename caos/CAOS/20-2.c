/* Взято с семинара 194 группы */
#include <stdio.h>
#include <signal.h>
#include <sys/time.h>
#include <stdlib.h>

volatile int count = 0;
volatile unsigned prime_num = 0;

void func(int sn) {
    count++;
    printf("%u\n", prime_num); fflush(stdout);
    if (count == 8) {
        exit(0);
    }
}

int is_prime(unsigned num) {
    for (unsigned i = 2; i * i <= num; ++i) {
        if (num % i == 0) {
            return 0;
        }
    }
    return 1;
}

int main(void) {
    unsigned low, high;
    scanf("%u%u", &low, &high);

    struct itimerval itime = {};
    itime.it_value.tv_sec = 0;
    itime.it_value.tv_usec = 100000;
    itime.it_interval.tv_sec = 0;
    itime.it_interval.tv_usec = 100000;

    signal(SIGVTALRM, func);
    setitimer(ITIMER_VIRTUAL, &itime, NULL);

    for (unsigned i = low; i < high; ++i) {
        if (is_prime(i)) {
            prime_num = i;
        }
    }
    printf("-1\n");
    return 0;
}
