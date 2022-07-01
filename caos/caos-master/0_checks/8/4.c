#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int get_argc(const char *cmd) {
    int argc = 0;
    int prev_space = 1;
    int i = 0;
    while (cmd[i]) {
        if (isspace(cmd[i])) {
            prev_space = 1;
        } else {
            if (prev_space) {
                ++argc;
            }
            prev_space = 0;
        }
        ++i;
    }
    return argc;
}

char **get_argv(char *str, int argc) {
    char **argv = malloc((argc + 1) * sizeof(char*));
    argv[argc] = NULL;
    char *tmp = str;
    char *delim = " \n\t\v\f\r";
    char *pch = strtok(tmp, delim);
    for (int i = 0; i < argc; ++i) {
        argv[i] = pch;
        pch = strtok(NULL, delim);
    }
    return argv;
}

int mysystem(const char *cmd) {
    int argc = get_argc(cmd);
    if (!argc) {
        return -1;
    }
    char *str = malloc(strlen(cmd) + 1);
    strcpy(str, cmd);
    char **argv = get_argv(str, argc);
    pid_t pid;
    int status;
    if ((pid = fork()) < 0) {
        free(argv);
        free(str);
        return -1;
    } else if (!pid) {
        if (execvp(argv[0], (char* const*)argv) == -1) {
            _exit(1);
        }
    } else {
        waitpid(pid, &status, 0);
    }
    free(argv);
    free(str);

    if (WIFSIGNALED(status)) {
        return WTERMSIG(status) + 1024;
    }
    return WEXITSTATUS(status);
}

#include <stdio.h>
int main(int argc, char ** argv) {
    char out [20000];

    strcpy(out, "(");
    strcat(out, argv[1]);
    strcat(out, "&&");
    strcat(out, argv[2]);
    strcat(out, " ) | ( ");
    strcat(out, argv[3]);
    strcat(out, " ; ");
    strcat(out, argv[4]);
    strcat(out, " ) > ");
    strcat(out, argv[5]);

    mysystem(out);
}