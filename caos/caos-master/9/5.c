#include <stdio.h>
int main() {
    int n, i;
    scanf("%d", &n);

    int * res;

    for (i = 0; i < n; ++i) {
        scanf("%d", res);
        ++res;
    }
    --res;

    for (i = n - 1; i >= 0; --i) {
        printf("%d\n", *res);
        --res;
    }
}
