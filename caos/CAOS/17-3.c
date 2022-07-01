/* Взято с семинара 194 группы */
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(int argc, char *argv[]){
    int fd[2];
    pipe(fd);
    if (!fork()) {
        dup2(fd[1], 1);
        close(fd[1]);
        close(fd[0]);
        if (!fork()) {
            execlp(argv[1], argv[1], NULL);
            _exit(1);
        }
        wait(NULL);
        if (!fork()) {
            execlp(argv[2], argv[2], NULL);
            _exit(1);
        }
        wait(NULL);
        return 0;
    }
    close(fd[1]);
    if (!fork()) {
        dup2(fd[0], 0);
        int file = creat(argv[4], 0600);
        dup2(file, 1);
        close(fd[0]);
        close(file);
        execlp(argv[3], argv[3], NULL);
        _exit(1);
    }
    close(fd[0]);
    wait(NULL);
    wait(NULL);
    return 0;
}
