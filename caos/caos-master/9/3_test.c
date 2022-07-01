#include <stdio.h>

int mystrcmp(const char *str1, const char *str2);

int main() {
    printf("%d\n", mystrcmp("adaa", "adaaa"));
    printf("%d\n", mystrcmp("adaaa", "adaa"));
}
