/* Взято с семинара 194 группы */
#include <stdio.h>
#include <sys/time.h>
#include <sys/signalfd.h>
#include <signal.h>
#include <unistd.h>

int main(void) {
    long long sec;
    long nsec;
    scanf("%lld%ld", &sec, &nsec);
    long long ttimer = sec * 1000 + (nsec + 500000) / 1000000;
    struct timeval tv;
    gettimeofday(&tv, NULL);
    long long tcur = (long long) tv.tv_sec * 1000 + (tv.tv_usec + 500) / 1000;
    if (ttimer <= tcur) {
        return 0;
    }
    ttimer -= tcur;
    struct itimerval itime;
    itime.it_interval = (struct timeval){0, 0};
    itime.it_value = (struct timeval){ttimer / 1000, (ttimer % 1000) * 1000};
    sigset_t mask;
    int sfd;
    struct signalfd_siginfo fdsi;
    sigemptyset(&mask);
    sigaddset(&mask, SIGALRM);
    if (sigprocmask(SIG_BLOCK, &mask, NULL) == -1) {
        fprintf(stderr, "Cannot block signal\n");
        return 1;
    }
    sfd = signalfd(-1, &mask, 0);
    if (sfd < 0) {
        return 1;
    }
    setitimer(ITIMER_REAL, &itime, NULL);
    if (read(sfd, &fdsi, sizeof(fdsi)) != sizeof(fdsi)) {
        return 1;
    }
    return 0;
}
