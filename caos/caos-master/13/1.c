#include <time.h>
#include <stdio.h>
#include <inttypes.h>

int main() {
    int32_t t_time;
    time_t mid;
    time_t current;

    while (scanf("%"SCNd32, &t_time) != EOF) {
        time(&current);

        if (__builtin_mul_overflow(t_time, 24 * 3600, &mid) ||
            __builtin_add_overflow(current, mid, &current)) {
            printf("OVERFLOW\n");
            continue;
        }

        struct tm * localTime = localtime(&current);

        char buf[20];

        strftime(buf, 20, "%F", localTime);

        printf("%s\n", buf);
    }
}
