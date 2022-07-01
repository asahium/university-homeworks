#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>

int process_args(char *input) {
    char * eptr;
    errno = 0;
    int64_t x = (int64_t) strtol(input, &eptr, 10);
    if (!*input || *eptr || errno) {
        return -1;
    } else if ((int8_t) x == x) {
        return 1;
    } else if ((int16_t) x == x) {
        return 2;
    } else if ((int32_t) x == x) {
        return 4;
    }
    return -1;
}


int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; ++i) {
        printf("%d\n", process_args(argv[i]));
    }
}