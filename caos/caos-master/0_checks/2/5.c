#include <stdint.h>
#include <stdio.h>

int max() {
    return 0x10000U - 0x10U - 1U;
}

void to_half_float(int value, unsigned short *hf) {
    if (value > max() || value < -max()) {
        *hf = value < 0 ? 0xfc00 : 0x7c00;
        return;
    }

    *hf = 0;

    if (!value)
        return;

    if (value < 0) {
        value *= -1;
        *hf |= 0x8000;
    }

    uint32_t t = value;
    int i = -1;
    while (t)
        t >>= 1, ++i;

    uint32_t sig = i;
    uint32_t m = value;

    int exp = sig;

    if (sig < 11) {
        m <<= 10 - sig;
    } else {
        m += 1u << (sig - 11);
        m >>= sig - 10;
    }

    if (m == 1 << 11)
        ++exp, m >>= 1;

    *hf |= (m ^ 0x400) | (exp + 15u) << 10;
}