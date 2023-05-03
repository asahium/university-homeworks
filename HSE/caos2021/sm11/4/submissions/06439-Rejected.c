// Comment by Judge: Строка 19: неправильная проверка кода завершения, используйте макросы WIFEXITED и WEXITSTATUS



#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <inttypes.h>

int main(void) {
    int x;
    pid_t p;
    pid_t pp = getpid();
    while (scanf("%d", &x) == 1) {
        p = fork();
        if (p < 0) {
            exit(1);
        }
        if (p) {
            int status;
            waitpid(p, &status, 0);
            if (!status) {
                printf("%d\n", x);
                fflush(stdout);
                exit(0);
            }
            if (getpid() == pp) {
                printf("-1");
                fflush(stdout);
                exit(0);
            }
            exit(1);
        }
    }
}
