#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <stdlib.h>

void p3() {
    printf("3 ");
    exit(0);
}

void p2() {
    pid_t p = fork();

    if (p < 0)
        exit(1);

    if (p == 0) {
        p3();
    }

    wait(NULL);
    printf("2 ");
    exit(0);
}

int main() {
    pid_t p = fork();

    if (p < 0)
        exit(1);

    if (p == 0) {
        p2();
    }

    wait(NULL);
    printf("1\n");
}