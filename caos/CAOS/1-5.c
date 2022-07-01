#include <stdio.h>
#include <ctype.h>

int main(void) {
    int c;
    int ans = 0;
    while ((c = getchar_unlocked()) != EOF) {
        if (isdigit(c)) {
            ans += c - '0';
        }
    }
    printf("%d\n", ans);
    return 0;
}