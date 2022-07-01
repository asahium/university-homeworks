#include <stdio.h>
#include <ctype.h>
#include <stdint.h>

enum {
    SYS_NUM = 7
};

int main(void) {
    int c;
    int parts[2] = {0, 0};
    long double val[3] = {0.0, 0.0, 1.0};
    while ((c = getchar_unlocked()) != EOF) {
        if (!(0 <= c - '0' && c - '0' < SYS_NUM)) {
            if (c == '.') {
                parts[1] = 1;
            } else if (parts[0]) {
                printf("%.10Lg\n", val[0] + val[1]);
                val[0] = 0.0;
                val[1] = 0.0;
                val[2] = 1.0;
                parts[0] = 0;
                parts[1] = 0;
            } else if (c != ' ' && c != '\n'){
                printf("Incorrect input\n");
                return 0;
            }
        } else if (parts[0]) {
            if (!parts[1]) {
                val[0] = SYS_NUM * val[0] + c - '0';
            } else {
                val[1] += (val[2] /= SYS_NUM) * (c - '0');
            }
        } else {
            parts[0] = 1;
            val[0] = c - '0';
        }
    }
    if (parts[0]) {
        printf("%.10Lg\n", val[0] + val[1]);
    }
    return 0;
}