#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

enum { BUF_SIZE = 8 };

int main(void) {
    for (int i = 0; i != 3; ++i) {
        if (!fork()) {
            char buf[BUF_SIZE];
            read(0, buf, sizeof(buf));
            long num = strtol(buf, NULL, 10);
            printf("%d %ld\n", i + 1, num * num);
            return 0;
        }
    }
    wait(NULL);
    wait(NULL);
    wait(NULL);
    return 0;
}