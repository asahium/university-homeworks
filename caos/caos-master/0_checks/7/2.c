#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(int argc, char ** argv) {
    pid_t pid = fork();

    if (pid < 0)
        exit(42);

    if (!pid) {
        int in_fd = open(argv[2], O_RDONLY);

        if (in_fd < 0)
            exit(42);

        dup2(in_fd, STDIN_FILENO);

        int out_fd = open(argv[3], O_WRONLY | O_CREAT | O_APPEND, 0660);

        if (out_fd < 0)
            exit(42);

        dup2(out_fd, STDOUT_FILENO);

        int out = open(argv[4], O_WRONLY | O_CREAT | O_TRUNC, 0660);

        if (out < 0)
            exit(42);

        dup2(out, STDERR_FILENO);

        close(out_fd);
        close(in_fd);

        execlp(argv[1], argv[1], NULL);

        exit(42);
    } else {
        int status;

        waitpid(pid, &status ,0);

        printf("%d", status);
    }

    wait(NULL);
}