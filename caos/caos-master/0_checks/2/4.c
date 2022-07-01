#include <stdio.h>
#include <inttypes.h>

const int MANTISSA = 53;
const int ORDER = 12;

int canBeDouble(int64_t input) {
    int i = 0;
    while (input % 2 == 0 && ++i < ORDER)
        input >>= 1;

    int res = input >> MANTISSA;
    return res == -1 || res == 0;
}

int main() {
    int64_t input;

    while (scanf("%" SCNd64, &input) != EOF)
        printf("%d\n", canBeDouble(input));
}
