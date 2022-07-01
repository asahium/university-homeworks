#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    pipe(fd);
    pid_t mommy = fork();
    if (mommy) {
        close(fd[0]);
        int input;
        while (scanf("%d", &input) == 1) {
            write(fd[1], &input, 4);
        }
        close(fd[1]);
        wait(NULL);
    } else {
        pid_t granny = fork();
        if (granny) {
            close(fd[0]);
            close(fd[1]);
            wait(NULL);
            exit(0);
        } else {
            close(fd[1]);
            int res;
            long long ans = 0;
            while (read(fd[0], &res, sizeof(int))) {
                ans += res;
            }
            close(fd[0]);
            printf("%lld", ans);
            fflush(stdout);
            exit(0);
        }
    }
}