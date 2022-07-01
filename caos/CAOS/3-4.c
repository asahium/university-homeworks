#include <stdint.h>
#include <inttypes.h>
#include <limits.h>

uint32_t fixed_mul(uint32_t a, uint32_t b, int n) {
    uint64_t res = (uint64_t)a * b;
    int bit = 0;
    uint64_t last_n_bit = res & ~((~0LLU) << n);
    if (n > 0) {
        if (last_n_bit > 1LLU << (n - 1)) {
            bit = 1;
        }
        else if (last_n_bit == ((1LLU << n) >> 1) && res & (1LLU << n)) {
            bit = 1;
        }
    }
    res >>= n;
    res += bit;
    if (res >= (uint64_t) ULONG_MAX) {
        return ULONG_MAX;
    }
    return res; 
}