#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    int N;

    scanf("%d", &N);

    for (int i = 0; i < N; ++i) {
        i == 0 ? printf("1") : printf(" %d", i + 1);
        fflush(STDIN_FILENO);

        if (i == N - 1) {
            printf("\n");
            exit(0);
        }

        pid_t p = fork();

        if (p < 0)
            exit(1);

        if (p) {
            break;
        }
    }

    wait(NULL);
    _exit(0);
}
