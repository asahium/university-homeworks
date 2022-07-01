#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

uint64_t mulmod(uint64_t a, uint64_t b, uint64_t c) {
    uint64_t o = 0;

    b = (b >= c) ? (b % c) : b;

    do {
        o += (a & 1) * (b - c * (b >= c - o));
        b += b - c * (b >= c - b);
    } while (a /= 2);

    return o;
}