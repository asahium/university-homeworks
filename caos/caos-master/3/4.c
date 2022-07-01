#include <stdio.h>
#include <inttypes.h>

int main() {
    int input;
    int i = -1;
    int j = 0;
    uint32_t target = 0;

    while (scanf("%x", &input) != EOF) {
        ++i;

        if (!(i % 17))
            continue;

        ++j;

        target <<= 8;
        target += input;

        if (!(j % 4)) {
            printf("%" PRIu32 "\n", target);
            target = 0;
        }
    }

}
