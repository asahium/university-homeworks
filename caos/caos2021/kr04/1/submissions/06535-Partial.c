// Total tests: 11
// Failed tests:
// 5 - Wrong answer



#include <ctype.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <math.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>
#include <limits.h>


int main(int argc, char* argv[]) {
    int fd = open(argv[1], O_RDWR | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd < 1) {
        return 1;
    }
    int rows = strtol(argv[2], NULL, 10);
    int cols = strtol(argv[3], NULL, 10);
    size_t sz = rows * cols * sizeof(double);
    if (ftruncate(fd, sz) == -1) {
        return -1;
    }
    
    void *addr = mmap(NULL, sz, PROT_WRITE, MAP_SHARED, fd, 0);
    if (addr == MAP_FAILED) {
        return -1;
    }
    double (*matrix)[cols] = addr;
    
    for (int i = 0; i != rows; ++i) {
        for (int j = 0; j != cols; ++j) {
            double a = sin((double) i);
            double b = cos((double) j / 2);
            matrix[i][j] = 2 * a + 4 * b;
        }
    }
    
    munmap(addr, sz);
    close(fd);
    return 0;
}
