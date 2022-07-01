#include <stdio.h>

int main() {
    unsigned int temp, t;
    unsigned int p1 = 0, p2 = 0, p3 = 0, p4 = 0, p5 = 0;

    while (scanf("%u", &temp) != EOF) {
        t = temp;
        p1 += temp & 127;
        temp >>= 7;
        p2 += temp & 127;
        temp >>= 7;
        p3 += temp & 127;
        temp >>= 7;
        p4 = temp & 127;
        temp >>= 7;
        p5 = temp & 127;

        if (t < (1 << 7)) {
            printf("%x", p1);
        } else if (t < (1 << 14)) {
            printf("%x %x", p1 | (1 << 7), p2);
        } else if (t < (1 << 21)) {
            printf("%x %x %x", p1 | (1 << 7), p2 | (1 << 7), p3);
        } else if (t < (1 << 28)) {
            printf("%x %x %x %x", p1 | (1 << 7), p2 | (1 << 7), p3 | (1 << 7), p4);
        } else {
            printf("%x %x %x %x %x", p1 | (1 << 7), p2 | (1 << 7), p3 | (1 << 7), p4 | (1 << 7), p5);
        }

        p1 = 0;
        p2 = 0;
        p3 = 0;
        p5 = 0;
        p4 = 0;

        printf("\n");
    }
}
