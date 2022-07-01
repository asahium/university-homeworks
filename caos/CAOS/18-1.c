/*Взято с семинара 194 группы*/
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