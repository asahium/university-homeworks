#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <sys/stat.h>

int main(int argc, char ** argv) {
    for (int j = 1; j < argc; ++j) {
        int fd = open(argv[j], O_RDONLY);

        if (fd == -1) {
            printf("-1\n");
            continue;
        }

        struct stat stat1;

        if (fstat(fd, &stat1) == -1) {
            close(fd);
            printf("-1\n");
            continue;
        }

        if (!stat1.st_size) {
            printf("0\n");
            continue;
        }

        void * mapped = mmap(NULL, stat1.st_size, PROT_READ, MAP_SHARED, fd, 0);

        if (mapped == MAP_FAILED) {
            printf("-1\n");
            close(fd);
            continue;
        }

        unsigned long long count = 0;

        char * m_mapped = (char *) mapped;

        for (long i = 0; i < stat1.st_size; ++i)
            if (m_mapped[i] == '\n')
                ++count;

        if (m_mapped[stat1.st_size - 1] != '\n')
            ++count;

        printf("%llu\n", count);

        close(fd);

        munmap(mapped, stat1.st_size);
    }
}
