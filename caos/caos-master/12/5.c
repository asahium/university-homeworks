#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <endian.h>

struct Data
{
    int16_t x;
    int64_t y;
};

int fd;
int A;

typedef struct Data Data;

void ch_seek(int i) {
    if (lseek(fd, 10 * i, SEEK_SET) < 0)
        exit(2);
}

void marshall(unsigned char *out, const Data *in) {
    int16_t a = htole16(in->x);
    memcpy(out, &a, 2);

    int64_t b = htole64(in->y);
    memcpy(out + 2, &b, 8);
}

void unmarshall(Data *out, const unsigned char *in) {
    memcpy(&out->x, in, 2);
    memcpy(&out->y, in + 2, 8);

    out->x = htole16(out->x);
    out->y = htole64(out->y);
}

Data b2d(int index) {
    ch_seek(index);

    int count = 0;

    unsigned char buf[10];

    while (count < 10) {
        int res = read(fd, buf + count, 10 - count);

        if (res <= 0)
            exit(2);

        count += res;
    }

    Data out;

    unmarshall(&out, buf);

    return out;
}

void d2b(Data out, int index) {
    ch_seek(index);

    int64_t prod = 0;

    if (__builtin_mul_overflow(out.x, A, &prod) ||
        __builtin_add_overflow(prod, out.y, &out.y))
        exit(3);

    int count = 0;

    unsigned char buf[10];
    marshall(buf, &out);

    while (count < 10) {
        int res = write(fd, buf + count, 10 - count);

        if (res <= 0)
            exit(2);

        count += res;
    }
}

void swap(int a, int b) {
    Data l = b2d(a);
    Data r = b2d(b);

    d2b(l, b);
    d2b(r, a);
}

int main(int _, char **argv) {
    fd = open(argv[1], O_RDWR);
    A = atoi(argv[2]);

    if (fd < 0)
        exit(2);

    int count = (lseek(fd, 0, SEEK_END) - lseek(fd, 0, SEEK_SET)) / 10;

    for (int i = 0; i < count / 2 + count % 2; ++i)
        swap(i, count - i - 1);

    close(fd);
}