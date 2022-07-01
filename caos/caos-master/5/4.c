#include <ctype.h>
#include <errno.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int32_t max = 0;

double min = INFINITY;

int found[2] = {0, 0};

void pae(int i) {
    fprintf(stderr, "valuable err\n");
    exit(1);
}

FILE * p_args(int c, char ** v) {
    if (c == 1)
        return stdin;
    if (c > 2)
        pae(1);

    FILE * input = fopen(v[1], "r");

    if (!input)
        pae(2);

    return input;
}

int process_double(char * str) {
    errno = 0;

    char *e;
    double num = strtod(str, &e);

    if (*e || errno)
        return 1;

    if (min == NAN)
        return 0;

    if (!found[1] || num < min) {
        found[1] = 1;
        min = num;
    } else if (num != num || min != min) {
        min = NAN;
    }

    return 0;
}

int process_int(char * string) {
    errno = 0;

    char *e;
    int64_t num = (int64_t)strtol(string, &e, 10);

    if (*e || !*string)
        return 1;

    if (errno && errno != ERANGE)
        return 1;

    if (errno == ERANGE || (num - (int32_t)num))
        return 0;

    if (!found[0] || num > max) {
        found[0] = 1;
        max = (int32_t) num;
    }

    return 0;
}

int main(int argc, char ** argv) {
    FILE * input = p_args(argc, argv);

    char buf[64];

    int c, i = 0;
    int empty = 1;

    while ((c = getc_unlocked(input)) != EOF) {
        if (((0 <= c && c <= 31) || c == 127) &&
            !(c == '\n' || c == '\t' || c == '\r'))
            pae(3);

        if (i == 63)
            pae(4);

        if (isspace(c) && !empty) {
            i = 0;
            empty = 1;
        } else if (i < 63) {
            buf[i] = c;
            buf[++i] = '\0';

            empty = 0;
            continue;
        }

        if (process_int(buf))
            process_double(buf);
    }

    if (!empty)
        if (process_int(buf))
            process_double(buf);


    if (found[0] + found[1] != 2)
        pae(7);

    printf("%d %.10g\n", max, min);

    fclose(input);
}