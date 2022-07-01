#include <stdio.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
    
int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; ++i) {
        int file = open(argv[i], O_RDONLY);
        if (file == -1) {
            printf("-1\n");
            continue;
        }
        struct stat st;
        int res = fstat(file, &st);
        if (res < 0) {
            close(file);
            printf("-1\n");
            continue;
        }
        if (!st.st_size) {
            printf("0\n");
            continue;
        }
        char *mapped = (char *)mmap(NULL, st.st_size, PROT_READ, MAP_SHARED, file, 0);
        if (mapped == MAP_FAILED) {
            printf("-1\n");
            close(file);
            continue;
        }
        unsigned long long count = 0;
        for (long i = 0; i < st.st_size; ++i) {
            if (mapped[i] == '\n') {
                ++count;
            }
        }
        if (mapped[st.st_size - 1] != '\n') {
            ++count;
        }
        close(file);
        munmap(mapped, st.st_size);
        printf("%llu\n", count);
    }
    return 0;
}