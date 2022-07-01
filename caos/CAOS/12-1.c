#include <stdio.h>
#include <time.h>
#include <inttypes.h>

int main(void) {
    int32_t days;
    time_t bubble;
    time_t cur;
    while (scanf("%"SCNd32, &days) == 1) {
        time(&cur);
        if (__builtin_mul_overflow(days, 60 * 60 * 24, &bubble) ||
            __builtin_add_overflow(bubble, cur, &cur)) {
            printf("OVERFLOW\n");
            continue;
        }
        char ans[14];
        struct tm *local = localtime(&cur);
        strftime(ans, 14, "%F", local);
        printf("%s\n", ans);
    }
}