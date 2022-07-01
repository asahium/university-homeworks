#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

int main(int argc, char *argv[]) {
    int file = open(argv[1], O_RDONLY);
    if (file < 0) {
        return 1;
    }
    off_t size = lseek(file, 0, SEEK_END);
    if (size == -1) {
        close(file);
        return 1;
    }
    double *mapped = (double*)mmap(NULL, size, PROT_READ, MAP_PRIVATE, file, 0);
    double ans = 0;
    size_t n = size / sizeof(double);
    for (size_t i = 0; i < n; ++i)
        ans += mapped[i];
    printf("%a\n", ans / n);
    munmap(mapped, size);
    close(file);
}