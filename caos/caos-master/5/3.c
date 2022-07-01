#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int classify(char *in) {
    char * e;
    errno = 0;

    int64_t num = (int64_t) strtol(in, &e, 10);

    if (*e || !*in || errno)
        return -1;

    if ((int8_t) num == num)
        return 1;
    if ((int16_t) num == num)
        return 2;
    if ((int32_t) num == num)
        return 4;

    return -1;
}


int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; ++i)
        printf("%d\n", classify(argv[i]));
}

