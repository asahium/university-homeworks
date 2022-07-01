#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* U+0020 = 0b100000 = 32 */

enum {
    SYS_NUM = 32,
    INIT_NUM = 50
};

typedef struct A {
    char * obj;
    unsigned long length;
    unsigned long cursize;
    unsigned long maxsize;
} A;

A init(void) {
    A str;
    str.obj = malloc(sizeof(char) * INIT_NUM);
    str.length = 0;
    str.cursize = 0;
    str.maxsize = INIT_NUM;
    str.obj[0] = '\0';
    return str;
}

void add(A * str, int c) {
    if (str->cursize == str->maxsize) {
        str->maxsize *= 2;
        str->obj = realloc(str->obj, str->maxsize + 1);
        if (str->obj == NULL) {
            fprintf(stderr, "error in realloc");
            free(str->obj);
            exit(1);
        }
    }
    str->obj[str->cursize] = c;
    str->cursize += 1;
    str->obj[str->cursize] = '\0';
}

int main(void) {
    A max = init();
    A cur = init();
    int c;
    while ((c = getchar_unlocked()) != EOF) {
        if (c > SYS_NUM) {
            add(&cur, c);
            if (c & 128) {
                add(&cur, getchar_unlocked());
            }
            if (c & 128 && c & 32) {
                add(&cur, getchar_unlocked());
            }
            if (c & 128 && c & 32 && c & 16) {
                add(&cur, getchar_unlocked());
            }
            cur.length += 1;
        } else if (cur.length) {
            if (cur.length > max.length) {
                max = cur;
            }
            cur = init();
        }
    }
    if (cur.length > max.length) {
        max = cur;
    }
    printf("%lu\n", max.length);
    if (max.length) {
        printf("%s\n", max.obj);
    }
    free(cur.obj);
    free(max.obj);
}