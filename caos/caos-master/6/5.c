#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct A
{
    char * obj;
    unsigned long size;
    unsigned long capacity;
    unsigned long count;
} US;


US init() {
    US str;
    str.obj = malloc(sizeof(char) * 400);
    str.size = 0;
    str.capacity = 400;
    str.count = 0;
    str.obj[0] = '\0';

    return str;
}

void append(US * str, int c) {
    if (str->size == str->capacity) {
        str->capacity *= 2;
        str->obj = realloc(str->obj, str->capacity + 1);
    }

    str->obj[str->size] = c;
    ++str->size;
    str->obj[str->size] = '\0';
}

int main() {
    US longest = init();
    US current = init();

    int c;
    while ((c = getchar_unlocked()) != EOF) {
        if (c > 32) {
            append(&current, c);

            if (c & 128)
                append(&current, getchar_unlocked());

            if (c & 128 && c & 32)
                append(&current, getchar_unlocked());

            if (c & 128 && c & 32 && c & 16)
                append(&current, getchar_unlocked());

            ++current.count;
        } else if (current.count) {
            if (current.count > longest.count) {
                US t = longest;
                longest = current;
                current = t;
            }

            current.count = 0;
            current.size = 0;
            current.obj[0] = '\0';
        }
    }

    if (current.count && current.count > longest.count) {
        US t = longest;
        longest = current;
        current = t;
    }

    printf("%lu\n", longest.count);

    if (longest.count)
        printf("%s\n", longest.obj);

    free(current.obj);
    free(longest.obj);
}
