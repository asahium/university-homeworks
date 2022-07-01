#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <inttypes.h>

int main() {
    pid_t pid;
    pid_t ppid = getpid();

    int i;

    while (scanf("%d", &i) == 1) {
        pid = fork();

        if (pid < 0)
            exit(1);

        if (pid) {
            int status;
            waitpid(pid, &status, 0);

            if (!status) {
                printf("%d\n", i);
                fflush(stdout);
                exit(0);
            }

            if (getpid() == ppid) {
                printf("-1");
                fflush(stdout);
                exit(0);
            }

            exit(1);
        }
    }
}
