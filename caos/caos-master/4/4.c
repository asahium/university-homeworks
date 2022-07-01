#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

uint32_t fixed_mul(uint32_t a, uint32_t b, int n) {
    uint64_t product = (uint64_t)a * b;

    int bit = 0;

    if (n > 0) {
        if ((product & (~((~0LLU) << n))) > ((1LLU << n) >> 1))
            bit = 1;
        else if ((product & (~((~0LLU) << n))) == ((1LLU << n) >> 1) && product & (1LLU << n))
            bit = 1;
    }

    product >>= n;
    product += bit;

    uint32_t max = ~0u;

    return product > (uint64_t) max ? max : product;
}
