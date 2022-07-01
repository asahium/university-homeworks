#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
    int fd = open(argv[1], O_RDWR);

    long long count = lseek(fd, 0, SEEK_END) / sizeof(long long);

    if (!count) {
        close(fd);
        return 0;
    }

    lseek(fd, 0, SEEK_SET);

    long long min;
    long long index = 0;

    read(fd, &min, sizeof(long long));

    long long buf;
    for (size_t i = 1; i < count; ++i) {
        read(fd, &buf, sizeof(long long));

        if (min > buf) {
            min = buf;
            index = i;
        }
    }

    lseek(fd, index * sizeof(long long), SEEK_SET);

    if ((unsigned long long)min != 1ull << (8 * sizeof(long long) - 1))
        min *= -1;

    write(fd, &min, sizeof(long long));
    close(fd);
}