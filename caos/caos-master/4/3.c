#include <stdint.h>

typedef union
{
    float as_float;
    uint32_t as_int;
} Float;

FPClass fpclassf(float value, int *sign) {
    Float _value;
    
    _value.as_float = value;

    uint32_t exp = (_value.as_int >> 23) & 0xFF;
    int mantissa = ((_value.as_int << 9) >> 9) ? 1 : 0;

    *sign = (_value.as_int >> 31) ? 1 : 0;

    if (!exp)
        return mantissa ? FFP_DENORMALIZED : FFP_ZERO;

    if (exp == 0xFF) {
        if (!mantissa)
            return FFP_INF;

        *sign = 0;
        return FFP_NAN;
    }

    return FFP_NORMALIZED;
}
