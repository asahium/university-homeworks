#include <unistd.h>
#include <sys/wait.h>

int ans(char *argv[], int num) {
    if (!fork()) {
        execlp(argv[num], argv[num], NULL);
        return 0;
    } else {
        int status;
        wait(&status);
        return WIFEXITED(status) && !WEXITSTATUS(status);
    }
}

int main(int _, char *argv[]) {
    if (ans(argv, 1) || ans(argv, 2)) {
        if (ans(argv, 3)) {
            return 0;
        }
    }
    return 1;
}