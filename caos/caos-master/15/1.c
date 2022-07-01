#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>

int main(int argc, char ** argv) {
    if (argc != 2) {
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);

    if (fd < 0)
        return 1;

    off_t size = lseek(fd, 0, SEEK_END);

    if (size == -1) {
        close(fd);
        return 1;
    }

    double *  mapped = (double *) mmap(NULL , size, PROT_READ, MAP_PRIVATE, fd, 0);

    double res = 0;
    size_t count = size / sizeof(double);

    for (size_t i = 0; i < count; ++i)
        res += mapped[i];
    printf("%a\n", res / count);
    munmap(mapped, size);

    close(fd);
}