#include <stdio.h>
#include <limits.h>
#include <inttypes.h>

uint32_t calc(char * str) {
    int count = 0, read = 0, neg = 1;
    int32_t num = 0;
    int64_t min = INT32_MAX, max = INT32_MIN;

    while (*str != '\0') {
        if (*str == ',') {
            if (num < min)
                min = num;

            if (num > max)
                max = num;

            num = 0;
            neg = 1;
            ++count;
            read = 1;
        } else {
            if (*str == '-') {
                neg = -1;
            } else {
                read = 0;
                num *= 10;
                num += neg * (int) (*str - 48);
            }
        }
        ++str;
    }

    if (!read) {
        if (num < min)
            min = num;

        if (num > max)
            max = num;
        ++count;
    }

    if (count == 1)
        return 1;

    return max - min + 1;
}

int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; ++i)
        printf("%" PRIu32 "\n", calc(argv[i]));
}
