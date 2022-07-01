/*Взято с семинара 191 группы*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        exit(1);
    }
    int fd[2];
    pipe(fd);
    if (!fork()) {
        dup2(fd[1], 1);
        close(fd[1]);
        close(fd[0]);
        execlp(argv[1], argv[1], NULL);
        _exit(1);
    }
    if (!fork()) {
        dup2(fd[0], 0);
        close(fd[1]);
        close(fd[0]);
        execlp(argv[2], argv[2], NULL);
        _exit(1);
    }
    close(fd[0]);
    close(fd[1]);
    wait(NULL);
    wait(NULL);
    return 0;
}