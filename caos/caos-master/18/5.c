#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void dac(int one, int two) {
    dup2(one, two);
    close(one);
}

void exec(char * arg) {
    execlp(arg, arg, NULL);
    _exit(1);
}

void kill_all(int *children, int size) {
    for (int i = 1; i < size; ++i)
        kill(children[i], SIGKILL);

    _exit(1);
}

int main(int count, char **argv) {
    int fd[2];

    if (pipe(fd) < 0)
        _exit(1);

    pid_t children[count];

    pid_t pid = fork();

    children[1] = pid;

    if (pid < 0) {
        _exit(1);
    } else if (!pid) {
        close(fd[0]);

        dac(fd[1], 1);
        exec(argv[1]);
    }

    close(fd[1]);

    int lst_in = fd[0];

    for (int i = 2; i < count; ++i) {
        if (pipe(fd) < 0)
            kill_all(children, i);

        children[i] = fork();

        if (children[i] < 0) {
            kill_all(children, i);
        } else if (!children[i]) {
            if (i < count - 1)
                dac(fd[1], 1);

            dac(lst_in, 0);

            if (i < count - 1)
                close(fd[0]);

            exec(argv[i]);
        }

        close(lst_in);

        if (i + 1 == count) {
            close(fd[0]);
            break;
        }

        close(fd[1]);
        lst_in = fd[0];
    }

    for (int i = 1; i < count; ++i)
        waitpid(-1, NULL, 0);
}