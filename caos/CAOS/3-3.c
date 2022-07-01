#include <stdint.h>

enum {
    MANTISSA = 23,
    MAXEXP = 0xFF,
    GETMANTISSA = 0x7FFFFF,
    BITS = 31
};

typedef union {
    float float_type;
    uint32_t int_type;
} Float;

FPClass fpclassf(float value, int *sign) {
    Float new_value;
    new_value.float_type = value;
    uint32_t exp = (new_value.int_type >> MANTISSA) & MAXEXP;
    int mantissa = new_value.int_type & GETMANTISSA;
    *sign = new_value.int_type >> BITS;
    if (exp == 0) {
        return mantissa ? FFP_DENORMALIZED : FFP_ZERO;
    }
    if (exp == MAXEXP) {
        if (mantissa == 0) {
            return FFP_INF;
        }
        *sign = 0;
        return FFP_NAN;
    }
    return FFP_NORMALIZED;
}