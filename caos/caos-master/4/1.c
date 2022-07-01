#include <stdio.h>

enum { SIGN = 1, EXP = 8, MANT = 23 };

int main() {
    float input;

    while (scanf("%f", &input) != EOF) {
        unsigned int* reint = (unsigned int*)&input;
        unsigned int sign = (*reint >> (EXP + MANT)) & 1;
        unsigned int exponent = (*reint >> MANT) & ((1 << EXP) - 1);
        unsigned int mantissa = *reint & ((1 << MANT) - 1);

        printf("%u %u %x\n", sign, exponent, mantissa);
    }
}
