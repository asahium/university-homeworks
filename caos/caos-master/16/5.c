#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <fcntl.h>

void process(char * name, int p_count, int p_index, int n_start, int n_count, int delta) {
    int fd = open(name, O_RDWR, 066);

    lseek(fd, 4 * p_index, SEEK_SET);

    int next = n_start + p_index * delta;

    for (int i = 0; i < n_count; ++i) {
        lseek(fd, 4 * (p_index + i * p_count), SEEK_SET);
        write(fd, &next, 4);
        next += p_count * delta;
    }

    close(fd);

    exit(0);
}

int main(int _, char ** args) {
    int total = atoi(args[1]);
    int start = atoi(args[3]);
    int delta = atoi(args[4]);
    int count = atoi(args[5]);

    close(creat(args[2], 0666));

    for (int p_index = 0; p_index < total; ++p_index)
        if (!fork())
            process(args[2], total, p_index, start, count, delta);

    for (int i = 0; i < total; ++i)
        wait(NULL);
}