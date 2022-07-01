#include <stdio.h>
#include <inttypes.h>

const int MANTISSA = 24;
const int ORDER = 9;

int canBeFloat(uint32_t input) {
    int i = 0;
    
    while (input % 2 == 0 && ++i < ORDER)
        input >>= 1;

    return (input >> MANTISSA) == 0;
}

int main() {
    uint32_t input;

    while (scanf("%" SCNu32, &input) != EOF)
        printf("%d\n", canBeFloat(input));
}
