#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    long long pos = 0;
    long long neg = 0;
    for (long long i = 0; i < argc; ++i) {
        if (atoi(argv[i]) > 0) {
            pos += atoi(argv[i]);
        } else {
            neg += atoi(argv[i]);
        }
    }
    printf("%lld\n%lld\n", pos, neg);
}