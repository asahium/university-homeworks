#include <stdio.h>
#include <ctype.h>
int main(void)
{
    long long a, b, i, j;
    int n;
    scanf("%lld", &a);
    scanf("%lld", &b);
    scanf("%d", &n);
    printf("%*s ", n, "");
    for(i = a; i < b;  i++) {
        if (i != b - 1) {
            printf("%*lld ", n, i);
        } else {
            printf("%*lld", n, i);
        }
    }
    printf("\n");
    for(i = a; i < b; i++) {
        printf("%*lld ", n, i);
        for(j = a; j < b;  j++) {
            if (j != b - 1) {
                printf("%*lld ", n, i * j);
            } else {
                printf("%*lld", n, i * j);
            }
        }
        printf("\n");
    }
    return 0;
}