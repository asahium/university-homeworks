#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void){
    int pid1 = fork();
    if (!pid1) {
        int pid2 = fork();
        if (!pid2) {
            printf("3 ");
        } else {
            wait(NULL);
            printf("2 ");
        }
    } else {
        wait(NULL);
        printf("1\n");
    }
    return 0;
}