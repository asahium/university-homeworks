#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    int fd[2];

    pipe(fd);
    pid_t p = fork();

    if (p) {
        close(fd[0]);

        int scanned;

        while (scanf("%d", &scanned) != EOF)
            write(fd[1], &scanned, 4);

        close(fd[1]);

        wait(NULL);
    } else {
        pid_t gp = fork();

        if (gp) {
            close(fd[0]);
            close(fd[1]);

            wait(NULL);
            exit(0);
        } else {
            close(fd[1]);

            int res;
            long long sum = 0;

            while (read(fd[0], &res, sizeof(int)))
                sum += res;W

            close(fd[0]);

            printf("%lld", sum);
            fflush(stdout);

            exit(0);
        }
    }
}
