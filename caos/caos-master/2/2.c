#include <stdio.h>
#include <ctype.h>

int main() {
    int a;
    int b;
    int n;

    scanf("%d %d %d", &a, &b, &n);

    printf("%*c", n, ' ');

    for (int i = a; i < b; ++i)
        printf(" %*d", n, i);

    printf("\n");

    for (int i = a; i < b; ++i) {
        printf("%*d", n, i);

        for (int j = a; j < b; ++j) {
            long res = (long) i * j;
            printf(" %*ld", n, res);
        }

        printf("\n");
    }
}
