#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(int argc, char ** argv) {
    int pipe_fd[2];

    pipe(pipe_fd);

    pid_t cmd1 = fork();

    if (!cmd1) {
        dup2(pipe_fd[1], 1);
        close(pipe_fd[0]);
        close(pipe_fd[1]);

        execlp(argv[1], argv[1], (char *) NULL);

        _exit(1);
    } else {
        pid_t cmd2 = fork();

        if (!cmd2) {
            waitpid(cmd1, NULL, 0);

            dup2(pipe_fd[1], 1);
            close(pipe_fd[0]);
            close(pipe_fd[1]);

            execlp(argv[2], argv[2], (char *) NULL);

            _exit(1);
        } else {
            pid_t cmd3 = fork();

            if (!cmd3) {
                int file = open(argv[4], O_WRONLY | O_CREAT | O_TRUNC, 0600);

                dup2(pipe_fd[0], 0);
                dup2(file, STDOUT_FILENO);
                close(pipe_fd[0]);
                close(pipe_fd[1]);

                execlp(argv[3], argv[3], (char *) NULL);

                _exit(1);
            } else {
                close(pipe_fd[0]);
                close(pipe_fd[1]);

                int status;
                while ((wait(&status)) > 0);

                exit(0);
            }
        }
    }
}
