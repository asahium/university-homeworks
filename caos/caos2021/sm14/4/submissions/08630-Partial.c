// Total tests: 15
// Failed tests:
// 1 - Run-time error
// 2 - Run-time error
// 3 - Run-time error
// 4 - Run-time error
// 5 - Run-time error
// 6 - Run-time error
// 7 - Run-time error
// 8 - Run-time error
// 9 - Run-time error
// 10 - Run-time error
// 11 - Run-time error
// 12 - Run-time error
// 13 - Run-time error
// 14 - Run-time error
// 15 - Run-time error



#include <inttypes.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

volatile int c = 0;

void func(int sn) {
    if (c < 4) {
        printf("%d\n", c);
        c++;
        fflush(stdout);
    } else {
        _exit(0);
    }
}

int main(int argc, char const *argv[]) {
    struct sigaction sa = {};
    sa.sa_flags = SA_RESTART;
    sa.sa_handler = func;
    sigaction(SIGINT, &sa, NULL);
    printf("%d\n", getpid());
    fflush(stdout);
    while (1) {
        pause();
    }
    return 0;
}
