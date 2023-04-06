#include <stdio.h>
int main(void)
{
    unsigned int a, b;
    scanf("%u%u", &a, &b);
    unsigned int average = (a / 2) + (b / 2) + (a % 2) * (b % 2); 
    printf("%u\n", average);
    return 0;
}