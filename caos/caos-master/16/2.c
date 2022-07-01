#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <inttypes.h>

void process(int id) {
    char buf[8];

    if (read(0, buf, 8) != 8)
        exit(1);

    int32_t n = strtol(buf, NULL, 10);
    printf("%d %" PRId32 "\n", id, n * n);
    exit(0);
}

int main() {
    for (int n = 0; n < 3; ++n) {
        if (!fork())
            process(n + 1);
    }

    for (int i = 0; i < 3; ++i)
        wait(NULL);
}

