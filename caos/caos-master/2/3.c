#include <stdio.h>
#include <ctype.h>

int main() {
    int c;
    int sum = 0;

    while ((c = getchar_unlocked()) != EOF)
        if (isdigit(c))
            sum += c - '0';

    printf("%d\n", sum);
}
