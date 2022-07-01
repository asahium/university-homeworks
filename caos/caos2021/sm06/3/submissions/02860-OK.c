#include <stdio.h>
#include <stdlib.h>

char *getline2(FILE *f) {
    size_t cursize = 0;
    size_t allocmem = 2;
    char *res = malloc(allocmem *sizeof(char));
    if (!res) {
        return NULL;
    }
    int c = getc(f);
    if (c == EOF) {
        free(res);
        return NULL;
    }
    res[cursize] = c;
    ++cursize;
    if (c == '\n') {
        res[cursize] = '\0';
        return res;
    }
    while ((c = getc(f)) != EOF) {
        if (cursize + 1 >= allocmem) {
            allocmem *= 2;
            char *newres = realloc(res, allocmem *sizeof(char));
            if (!newres) {
                free(res);
                return NULL;
            }
            res = newres;
        }
        res[cursize] = c;
        ++cursize;
        if (c == '\n') {
            res[cursize] = '\0';
            return res;
        }
    }
    res[cursize] = '\0';
    return res;
}
