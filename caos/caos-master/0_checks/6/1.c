#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char ** argv) {
    if (argc < 3)
        return 1;

    int ord = 0;
    int fri = 0;

    time_t raw;
    time(&raw);

    struct tm * local = localtime(&raw);

    local->tm_mday = 1;
    
    local->tm_year = atoi(argv[1]) - 1900;
    local->tm_mon = atoi(argv[2]) - 1;

    local->tm_hour = 0;
    local->tm_min = 0;
    local->tm_sec = 0;

    local->tm_isdst = -1;

    time_t start = mktime(local);

    while (1) {
        local = localtime(&start);

        if (local->tm_mon != atoi(argv[2]) - 1) {
            break;
        }

        int week_day = local->tm_wday;

        if (week_day >=1 && week_day <= 4) {
            ++ord;
        } else if (week_day == 5) {
            ++fri;
        }

        start += 86400;
    }

    printf("%d", 8 * ord + 6 * fri);
}