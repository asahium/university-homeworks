#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);

    for (int j = 1; j < n; ++j)
        printf("0%c", j < n - 1 ? ' ' : '\n');

    int current[n], prev[n];

    for (int j = 1, k = -1; j < n; ++j, k = -1) {
        while (++k < n && (k * j - 1) % n);

        current[j] = k;

        printf("%d%c", prev[j] = k, j < n - 1 ? ' ' : '\n');
    }

    for (int i = 2; i < n; ++i)
        for (int j = 1; j < n; ++j)
            printf("%d%c", prev[j] = (current[j] + prev[j]) % n,
                   j < n - 1 ? ' ' : '\n');
}