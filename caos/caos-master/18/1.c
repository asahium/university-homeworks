#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char ** argv) {
    if (argc < 3)
        exit(1);

    int fd[2];
    int in, out;

    if (pipe(fd) < 0)
        exit(1);

    in = fork();

    if (in < 0)
        exit(1);

    if (!in) {
        dup2(fd[1], 1);

        close(fd[0]);
        close(fd[1]);

        execlp(argv[1], argv[1], (char *) NULL);

        _exit(1);
    }

    out = fork();

    if (out < 0)
        exit(1);

    if (!out) {
        dup2(fd[0], 0);

        close(fd[0]);
        close(fd[1]);

        execlp(argv[2], argv[2], (char *) NULL);

        _exit(1);
    }

    close(fd[0]);
    close(fd[1]);

    wait(NULL);
    wait(NULL);

    return 0;
}
