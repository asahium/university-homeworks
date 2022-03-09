#include <stdio.h>

enum { 
    SIGN = 1, 
    EXP = 8, 
    MANTISSA = 23 
};

int main() {
    float input;
    while (scanf("%f", &input) == 1) {
        unsigned int* reint = (unsigned int*)&input;
        unsigned int sign = (*reint >> (EXP + MANTISSA)) & 1;
        unsigned int exp = (*reint >> MANTISSA) & ((1 << EXP) - 1);
        unsigned int mantissa = *reint & ((1 << MANTISSA) - 1);
        printf("%u %u %x\n", sign, exp, mantissa);
    }
    return 0;
}
