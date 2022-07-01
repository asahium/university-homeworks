/* Взято с семинара 194 группы*/
#include <fcntl.h>
#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
    uint16_t num;
    unsigned char buf[2];

    int fd = open(argv[1], O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) {
        perror(argv[0]);
        return 1;
    }

    while (scanf("%"SCNu16, &num) == 1) {
        buf[0] = num >> CHAR_BIT;
        buf[1] = num;
        int written = write(fd, buf, sizeof(buf) / sizeof(buf[0]));
        if (written < 0) {
            perror(argv[0]);
            return 1;
        }
    }

    close(fd);

    return 0;
}
