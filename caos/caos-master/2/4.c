#include <ctype.h>
#include <stdint.h>
#include <stdio.h>

int main() {
    int flags[2] = {0, 0};
    long double val[3] = {0, 0, 1.0};

    int c;

    while ((c = getchar_unlocked()) != EOF) {
        if (!isdigit(c)) {
            if (c == '.') {
                flags[1] = 1;
            } else if (flags[0]) {
                printf("%.10Lg\n", val[0] + val[1]);
                val[0] = 0;
                val[1] = 0;
                val[2] = 1.0;
                flags[0] = 0;
                flags[1] = 0;
            }
        } else if (flags[0]) {
            if (flags[1])
                val[1] += (c - '0') * (val[2] /= 7);
            else
                val[0] = 7 * val[0] + (c - '0');
        } else {
            flags[0] = 1;
            val[0] = c - '0';
        }
    }

    if (flags[0])
        printf("%.10Lg\n", val[0] + val[1]);
}
