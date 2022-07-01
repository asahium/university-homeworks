#include <ctype.h>
#include <stdio.h>

char process(int c) {
    int r = 0;

    if (isdigit(c))
        r = c - '0' + 1;
    else if (islower(c))
        r = c - 'a' + 11;
    else if (isupper(c))
        r = c - 'A' + 37;

    r &= ~(1 << 2);

    r & (1 << 3) ? (r &= ~(1 << 3)) : (r |= (1 << 3));

    if (!r)
        return '@';

    if (1 <= r && r <= 10)
        return '0' + r - 1;

    if (11 <= r && r <= 36)
        return 'a' + r - 11;

    if (37 <= r && r <= 62)
        return 'A' + r - 37;

    return '#';
}

int main() {
    int c;

    while ((c = getchar()) != EOF)
        if (isdigit(c) || islower(c) || isupper(c))
            printf("%c", process(c));
}