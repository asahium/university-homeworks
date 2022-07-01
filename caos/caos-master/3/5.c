#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <ctype.h>

int op(int c) {
    return c == '|' || c == '&' || c == '^';
}

int ord(int c) {
    if ('a' <= c && c <= 'z')
        return 'a' - c + 26;

    if ('A' <= c && c <= 'Z')
        return 'A' - c + 52;

    if ('0' <= c && c <= '9')
        return '0' - c + 62;

    return -1;
}

char chr(int i) {
    if (i <= 26)
        return 'a' + 26 - i;
    if (i <= 52)
        return 'A' + 52 - i;
    if (i <= 62)
        return '0' + 62 - i;

    return -1;
}

void print(uint64_t set) {
    int empty = 1;

    for (int i = 62; i >= 1; --i) {
        if ((set & ((uint64_t) 1 << i))) {
            printf("%c", chr(i));
            empty = 0;
        }
    }

    printf("%c\n", empty ? '#' : ' ');
}

int main() {
    uint64_t stack[1002];
    uint64_t current = 0;

    int i = -1;
    int c;

    while ((c = getchar_unlocked()) != EOF) {
        if (c == '#')
            stack[++i] = 0;
        else if (c == '~')
            stack[i] = ~stack[i];
        else if (op(c)) {
            if (c == '|')
                stack[i - 1] |= stack[i];
            if (c == '&')
                stack[i - 1] &= stack[i];
            if (c == '^')
                stack[i - 1] ^= stack[i];
            --i;
        } else if (isalnum(c)) {
            current |= (uint64_t)1 << ord(c);
        } else if (current) {
            stack[++i] = current;
            current = 0;
        }
    }

    if (current)
        stack[++i] = current;

    print(i >= 0 ? stack[i] : 0);
}
