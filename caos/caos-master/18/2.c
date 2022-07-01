#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    int fd[2];

    pipe(fd);
    pid_t parent = fork();

    if (parent) {
        close(fd[0]);

        int scanned;

        while (scanf("%d", &scanned) != EOF)
            write(fd[1], &scanned, 4);

        close(fd[1]);

        wait(NULL);
    } else {
        pid_t grandparent = fork();

        if (grandparent) {
            close(fd[0]);
            close(fd[1]);

            wait(NULL);
            exit(0);
        } else {
            close(fd[1]);

            int result;
            long long sum = 0;

            while (read(fd[0], &result, sizeof(int)))
                sum += result;

            close(fd[0]);

            printf("%lld", sum);
            fflush(stdout);

            exit(0);
        }
    }
}