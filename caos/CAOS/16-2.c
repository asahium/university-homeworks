#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

int mysys(const char *str) {
    pid_t pid = fork();
    if (pid < 0) {
        return -1;
    }
    if (pid) {
        int status;
        waitpid(pid, &status, 0);
        if (WIFSIGNALED(status)) {
            return 128 + WTERMSIG(status);
        }
        return WEXITSTATUS(status);
    } else  {
        execlp("/bin/sh", "sh", "-c", str, NULL);
        _exit(127);
    }
}