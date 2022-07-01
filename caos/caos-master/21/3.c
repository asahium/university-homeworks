#include <sys/time.h>
#include <time.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/eventfd.h>

char * number;
int * counter;

int base;

int fd[2];

void increment(int j) {
    printf("%d %s\n", j, number);
    fflush(stdout);

    int len = strlen(number);
    int carry = 1;

    for (int i = 0; i < len; ++i) {
        number[i] += carry;

        if (number[i] != '0' + base)
            carry = 0;
        else {
            number[i] = '0';
            carry = 1;
        }
    }

    if (carry) {
        number[len] = '1';
        number[len + 1] = '\0';
    }

    ++*counter;
}


int main(int argc, char **argv) {
    int n = atoi(argv[1]);
    base = atoi(argv[2]);

    void * data = mmap(NULL, 4096 * sizeof(char) + sizeof(int),
            PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);

    counter = data;
    *counter = 1;

    number = data + sizeof(int);

    strcpy(number, argv[3]);

    fd[0] = eventfd(0, EFD_SEMAPHORE);
    fd[1] = eventfd(0, EFD_SEMAPHORE);

    if (n) {
        if (!fork()) {
            uint64_t t = 1;

            increment(1);

            write(fd[1], &t, sizeof(t));

            while (*counter < n) {
                read(fd[0], &t, sizeof(t));

                increment(1);

                write(fd[1], &t, sizeof(t));
            }

            exit(0);
        }
        if (!fork()) {
            uint64_t t;

            while (*counter < n) {
                read(fd[1], &t, sizeof(t));

                increment(2);

                write(fd[0], &t, sizeof(t));
            }

            exit(0);
        }

        waitpid(-1, NULL, 0);
        waitpid(-1, NULL, 0);
    }

    printf("Done\n");

    munmap(data, 4096 * sizeof(char) + sizeof(int));
}