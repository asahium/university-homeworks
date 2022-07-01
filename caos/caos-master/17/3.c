#include <unistd.h>
#include <sys/wait.h>

int res(char **a, int i) {
    if (!fork()) {
        execlp(a[i], a[i], NULL);
        return 0;
    } else {
        int status;
        wait(&status);
        return WIFEXITED(status) && !WEXITSTATUS(status);
    }
}

int main(int _, char ** a) {
    return res(a, 1) || res(a, 2) ? res(a, 3) ? 0 : 1 : 1;
}