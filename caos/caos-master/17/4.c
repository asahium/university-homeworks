#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <limits.h>

char * init_dir() {
    char * res = getenv("XDG_RUNTIME_DIR");

    if (!res)
        res = getenv("TMPDIR");

    return res;
}

void init_fn(char * filename) {
    time_t ut;
    time(&ut);

    char t[12];
    sprintf(t, "%ld", ut);

    strcat(filename, t);
}

void init_salt(char * filename) {
    char salt_str[11];
    srand(time(NULL));
    sprintf(salt_str, "%d", rand() % 100000000);
    strcat(filename, salt_str);
}

void write_file(char * path, int c, char ** args) {
    int out = creat(path, 0700);

    write(out, "#!/usr/bin/env python3\n", 23 * sizeof(char));
    write(out, "from os import remove\n", 22 * sizeof(char));
    write(out, "from sys import argv\n", 21 * sizeof(char));
    write(out, "print(", 6 * sizeof(char));

    for (int i = 1; i < c; ++i) {
        write(out, args[i], sizeof(char) * strlen(args[i]));

        if (i != c - 1)
            write (out, "*", sizeof(char));
    }

    write(out, ")\nremove(argv[0])", 17 * sizeof(char));

    close(out);
}

int main(int c, char ** arg) {
    char * dir = init_dir();

    char path[PATH_MAX];

    if (dir) {
        strcpy(path, dir);
        strcat(path, "/");
    } else {
        strcpy(path, "/tmp/");
    }

    init_fn(path);
    init_salt(path);
    strcat(path, ".py");

    write_file(path, c, arg);

    execlp(path, path, NULL);
}