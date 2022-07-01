#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdio.h>
#include <math.h>

int main(int argc, char ** argv)  {
    int rows = atoi(argv[2]);
    int cols = atoi(argv[3]);

    int fd = open(argv[1], O_RDWR | O_CREAT | O_TRUNC, 0600);

    if (fd < 0)
        return 1;

    long long size = rows * cols * sizeof(double);

    ftruncate(fd, size);

    double **  mapped = (double ** ) mmap(0, size,
            PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (mapped == MAP_FAILED) {
        close(fd);
        return 1;
    }

    double out[rows][cols];

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            double res = 2*sin((double)i) + 4*cos((double)j / 2);
            out[i][j] = res;
        }
    }

    memcpy(mapped, out, size);
    munmap(mapped, size);

    close(fd);
}