#include <stdio.h>

void myhypot(double a, double b, double* r);

int main() {
    double a = 3.0;
    double b = 4.0;
    double res = 0;
    myhypot(a, b, &res);
    printf("%lf\n", res);
}
