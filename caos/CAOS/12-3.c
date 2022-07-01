#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    FILE *input = fopen(argv[1], "r");
    time_t start = 0;
    int year, mon, day, hour, min, sec;
    struct tm local;
    while (fscanf(input, " %d/%d/%d %d:%d:%d ", &year, &mon,
    &day, &hour,&min, &sec) == 6) {
        local.tm_sec = sec;
        local.tm_min = min;
        local.tm_hour = hour;
        local.tm_mday = day;
        local.tm_mon = mon - 1;
        local.tm_year = year - 1900;
        local.tm_isdst = -1;
        time_t end = mktime(&local);
        if (start != 0) {
            printf("%ld\n", end - start);
        }
        start = end;
    }
    fclose(input);
}