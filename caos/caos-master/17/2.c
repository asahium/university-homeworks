#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int mysys(const char *str) {
    pid_t child = fork();

    if (child < 0)
        return -1;

    if (child) {
        int status;
        waitpid(child, &status, 0);

        if (WIFSIGNALED(status))
            return WTERMSIG(status) + 128;

        return WEXITSTATUS(status);
    } else  {
        execlp("/bin/sh", "sh", "-c", str, NULL);
        _exit(127);
    }
}