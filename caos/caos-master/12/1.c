#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    int file = open(argv[1], O_WRONLY | O_CREAT | O_TRUNC, 0600);
    unsigned short input;

    while (scanf("%hu", &input) != EOF) {
        unsigned char buf[2];

        buf[1] = input & ((1 << 8) - 1);
        input >>= 8;
        buf[0] = input;

        size_t o = write(file, buf, 2);

        if (o != 2)
            return 1;
    }

    close(file);
}
