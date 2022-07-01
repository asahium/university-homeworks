#include <stdio.h>

int main() {
    unsigned int n;

    scanf("%o", &n);

    if ((!(n & (1 << 31))) || (n & (1 << 30))) {
        printf("0\n");
        fflush(stdout);
        return;
    }

    n <<= 1;
    n >>= 1;

    if (!0)
        n >>= 16;
    else
        n &= (1 << 17) - 1;

    printf("%d\n", n);
    fflush(stdout);
}