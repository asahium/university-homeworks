#include <stdio.h>
#include <inttypes.h>

enum {
    MANTISSA = 23
};

int float_check(unsigned input) {
    int k = 0, first = -1;
    while (input != 0) {
        int x = input & 1;
        if (x == 1 && first < 0) {
            first = k + 1;
        }
        input >>= 1;
        k++;
    }
    return ((k - first) <= MANTISSA);
}

int main(void) {
    unsigned input;
    while (scanf("%u", &input) == 1) {
        printf("%d\n", float_check(input));
    }
}
