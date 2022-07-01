#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdio.h>
#include <math.h>

int compar(const void *a, const void *b)
{
    if (*(double*)a > *(double*)b)
        return 1;
    else return *(double *) a < *(double *) b ? -1 : 0;
}

int main(int argc, char ** argv)  {
    int fd = open(argv[1], O_RDONLY, 0600);

    if (fd < 0)
        return 1;

    off_t size = lseek(fd, 0, SEEK_END);

    long count = size / sizeof(double);
    long N = count / 10;

    if (size == -1) {
        close(fd);
        return 2;
    }

    if (size == 0) {
        printf("0");
        return 0;
    }

    lseek(fd, 0, SEEK_SET);

    double * mapped = mmap(0, size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);

    if (mapped == MAP_FAILED) {
        close(fd);
        return 3;
    }

    double * mapped_useful = &mapped[N];

    long mapped_count = count - 2 * N;
    qsort(mapped_useful, mapped_count, sizeof(double), compar);

    double result = 0;

    long M = mapped_count / 10;
    long looped_count = mapped_count - 2 * M;

    for (long i = 0; i < looped_count; ++i)
        result += mapped_useful[i + M] / looped_count;

    printf("%.10g", result);

    munmap(mapped, size);
    close(fd);
}