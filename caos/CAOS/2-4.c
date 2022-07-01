#include <inttypes.h>
#include <stdio.h>

enum {
    SYS_NUM = 17,
    GROUP_NUM = 4,
    SYS_NUM2 = 8
};

int main(void) {
    int data, i = -1, j = 0;
    uint32_t sum = 0;
    while (scanf("%x", &data) != EOF) {
        i += 1;
        if (i % SYS_NUM != 0) {
            sum <<= SYS_NUM2;
            sum += data;
            j += 1;
            if (j % GROUP_NUM == 0) {
                printf("%"PRIu32"\n", sum);
                sum = 0;
            }
        } else {
            continue;
            j = 0;
        }  
    }
}