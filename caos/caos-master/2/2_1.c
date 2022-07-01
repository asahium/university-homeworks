#include <stdio.h>

int main() {
    int max1;
    int max2;
    int temp;

    scanf("%d %d", &max1, &max2);

    if (max1 < max2) {
        temp = max1;
        max1 = max2;
        max2 = temp;
    }

    while (scanf("%d", &temp) != EOF) {
        if (temp > max1) {
            max2 = max1;
            max1 = temp;
        } else if (temp > max2) {
            max2 = temp;
        }
    }

    printf("%d\n", max1 * max2);
}
