#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <<stdint.h>>

volatile sig_atomic_t mode = 0; 

void sig_handler(int sn) {
    if (sn == SIGUSR1) {
        mode = 0;
    }
    if (sn == SIGUSR2) {
        mode = 1;
    }

}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = sig_handler;
    sa.sa_flags = SA_RESTART;
    sigaction(SIGUSR1, &sa, NULL);
    sigaction(SIGUSR2, &sa, NULL);
    int64_t a;
    printf("%d\n", getpid());
    fflush(stdout);
    while (scanf("%d", &a) == 1) {
        if (mode == 0) {
            printf("%d\n", -a);
        } else {
            printf("%d\n", a * a);
        }
        fflush(stdout);
    }

}
