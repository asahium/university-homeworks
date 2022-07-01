#include <stdio.h>
int main() {
    unsigned long long size = 0;
    unsigned int l, r;
    while (scanf("%x-%x %*[^\n]%*c", &l, &r) != EOF)
        size += r - l;
    printf("%llu", size);
}
