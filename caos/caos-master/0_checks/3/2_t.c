#include <stdio.h>

int process(int * res, signed char a, int b);

int main () {
    int res = -1;
    printf("%d ", process(&res, 10, 5));
    printf("%d\n", res);
}
