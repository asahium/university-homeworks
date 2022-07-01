#include <wchar.h>
#include <wctype.h>
#include <locale.h>
#include <stdio.h>

int main() {
    setlocale(LC_ALL, "");

    int digits = 0;
    int lower = 0;
    int upper = 0;

    wchar_t c;
    
    while ((c = fgetwc(stdin)) != EOF) {
        digits += iswdigit(c);
        lower += iswlower(c);
        upper += iswupper(c);
    }

    printf("%d\n%d\n%d\n", digits, upper, lower);
}
