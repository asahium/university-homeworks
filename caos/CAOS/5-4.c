#include <stdio.h>
#include <wchar.h>
#include <wctype.h>
#include <locale.h>

int min(int x, int y) {
    return (x < y ) ? x : y;
}

int main(void) {
    setlocale(LC_ALL, "");
    int digits = 0;
    int low = 0;
    int up = 0;
    wint_t c; 
    while ((c = fgetwc(stdin)) != WEOF) {
        digits += iswdigit(c);
        low += min(1, iswlower(c));
        up += min(1, iswupper(c));
    }
    printf("%d\n%d\n%d\n", digits, up, low);
}