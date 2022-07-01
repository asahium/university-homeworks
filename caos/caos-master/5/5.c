#include <stdlib.h>
#include <stdio.h>

char * getline2(FILE * f) {
    char * res = malloc(2 * sizeof(char));

    if (!res)
        return NULL;

    size_t size = 0;
    size_t allocated = 2;

    int c = getc(f);

    if (c == EOF) {
        free(res);
        return NULL;
    }

    res[0] = c;
    ++size;

    if (c == '\n') {
        res[1] = '\0';
        return res;
    }

    while ((c = getc(f)) != EOF) {
        if (size + 1 >= allocated) {
            allocated *= 2;

            char * res_r = realloc(res, allocated * sizeof(char));

            if (!res_r) {
                free(res);
                return NULL;
            }

            res = res_r;
        }

        res[size++] = c;

        if (c == '\n')
            break;
    }

    res[size] = '\0';

    return res;
}