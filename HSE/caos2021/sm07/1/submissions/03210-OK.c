#include<inttypes.h>

int32_t satsum(int32_t v1, int32_t v2) {
    int32_t sum;
    if (__builtin_add_overflow(v1, v2, &sum)) {
        uint32_t u = 0 - 1U;
        if (v1 > 0 && v2 > 0) {
            return u / 2;
        } else {
            return ~(u / 2);
        }
    }
    return sum;
}
