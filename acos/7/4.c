#include <ctype.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int imull_overflow(int64_t a, int64_t b, int64_t *res) {
    int sign = 0;

    if ((a < 0 && b > 0) || (a > 0 && b < 0)) {
        sign = 1;
    }
    int f = 0;
    
    uint64_t a_new = (uint64_t) a;
    uint64_t b_new = (uint64_t) b;
    uint64_t res_new = a_new * b_new;
    int64_t ans = (int64_t) res_new;
    *res = ans;

    if (sign == 0) {
        if (b != 0 && ((b > 0 && a > INT64_MAX / b) || (b < 0 && a < INT64_MAX / b))) {
            f = 1;
        }
    } else {
        if (b != 0 && ((b > 0 && a < INT64_MIN / b) || (b < 0 && b < INT64_MIN / a))) {
            f = 1;
        }
    }
    return f;
}

