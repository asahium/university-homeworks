#include<inttypes.h>

uint32_t satsum(uint32_t v1, uint32_t v2) {
    if (v1 + v2 < v1) {
        uint32_t res = 0 - 1U;
        return res;
    }

    return v1 + v2;
}
