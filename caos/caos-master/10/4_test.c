#include <stdio.h>

float dot_product(int n, const float * a, const float * b);

int main() {
    float a[] = {2.5f, 1.0f};
    float b[] = {-4.0f, 1.0f};
    int n = 2;

    printf("%f\n", dot_product(n, a, b));

}
