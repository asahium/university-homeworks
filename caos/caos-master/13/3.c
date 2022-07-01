#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    FILE * input = fopen(argv[1], "r");

    time_t start = 0;
    
    int y, mo, d, h, m, s;

    struct tm local;

    while (fscanf(input, " %d/%d/%d %d:%d:%d ", &y, &mo, &d, &h, &m, &s) != EOF) {
        local.tm_sec = s;
        local.tm_min = m;
        local.tm_hour = h;
        local.tm_mday = d;
        local.tm_mon = mo - 1;
        local.tm_year = y - 1900;
        local.tm_isdst = -1;

        time_t end = mktime(&local);
        
        if (start != 0)
            printf("%ld\n", end - start);

        start = end;
    }

    fclose(input);
}
