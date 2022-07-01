
#include <fcntl.h>
#include <limits.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc == 1) {
        _exit(0);
    }
    char *args[argc];
    int j = 0;
    int status;
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "END") == 0) {
            args[j] = NULL;
            if (!fork()) {
                execvp(args[0], args);
                _exit(1);
            }
            waitpid(-1, &status, 0);
            if (WEXITSTATUS(status) != 0 || WIFSIGNALED(status)) {
                _exit(1);
            }
            j = 0;
            continue;
        }
        args[j] = argv[i];
        ++j;
    }
    if (strcmp(argv[argc - 1], "END") == 0) {
        _exit(0);
    }
    args[j] = NULL;
    if (!fork()) {
        execvp(args[0], args);
        _exit(1);
    }
    waitpid(-1, &status, 0);
    if (WEXITSTATUS(status) != 0 || WIFSIGNALED(status)) {
        _exit(1);
    }
}