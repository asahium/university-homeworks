#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <ctype.h>
#include <string.h>

int mysystem(const char *cmd) {
    while (cmd && isspace(*cmd))
        ++cmd;

    if (!strlen(cmd))
        return -1;

    // parse file

    size_t file_size = 0;

    const char * temp = cmd;
    while (*temp != '\0' && !isspace(*temp)) {
        ++temp;
        ++file_size;
    }

    char file[file_size + 1];

    for (int i = 0; i < file_size; ++i) {
        file[i] = *cmd;
        ++cmd;
    }

    file[file_size] = '\0';

    while (*cmd != '\0' && isspace(*cmd))
        ++cmd;

    //parse args

    char ** args;

    if (*cmd == '\0') {
        args = malloc(2 * sizeof(char *));

        args[0] = malloc((file_size + 1) * sizeof(char));

        for (int k = 0; k < file_size + 1; ++k) {
            args[0][k] = file[k];
        }

        args[1] = NULL;
    } else {
        args = malloc((strlen(cmd) + 2) * sizeof(char * ));

        args[0] = malloc((file_size + 1) * sizeof(char));

        for (int k = 0; k < file_size + 1; ++k) {
            args[0][k] = file[k];
        }

        int lis = 0;
        int i = 1;

        while (*cmd != '\0') {
            if (lis) {
                while (*cmd != '\0' && isspace(*cmd))
                    ++cmd;

                lis = 0;
            } else {
                const char * temp_str = cmd;
                size_t elem_size = 0;
                while (*temp_str != '\0' && !isspace(*temp_str)) {
                    ++temp_str;
                    ++elem_size;
                }

                args[i] = malloc(sizeof(char) * elem_size);

                int j = 0;
                while (*cmd != '\0' && !isspace(*cmd)) {
                    args[i][j] = *cmd;
                    ++j;
                    ++cmd;
                }

                args[i][j] = '\0';
                lis = 1;
                ++i;
            }
        }

        args[i] = NULL;
    }

    //fork

    pid_t child = fork();

    if (child < 0)
        return -1;

    if (child) {
        int status;
        waitpid(child, &status, 0);

        if (WIFSIGNALED(status))
            return WTERMSIG(status) + 1024;

        return WEXITSTATUS(status);
    } else  {
        execvp(file, args);
        _exit(1);
    }
}