#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    int file = open(argv[1], O_WRONLY | O_CREAT | O_TRUNC, 0600);
    unsigned input;

    while (scanf("%u", &input) != EOF) {
        unsigned char buf[4];

        buf[3] = input & ((1 << 8) - 1);
        input >>= 8;
        buf[2] = input & ((1 << 8) - 1);
        input >>= 8;
        buf[1] = input & ((1 << 8) - 1);
        input >>= 8;
        buf[0] = input;

        size_t o = write(file, buf, 4);

        if (o != 4)
            return 1;
    }

    close(file);
}

