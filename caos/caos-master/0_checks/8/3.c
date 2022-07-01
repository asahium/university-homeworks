#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
#include <math.h>

double x0;
double dx;
int n;

int fd1[2];
int fd2[2];

FILE * read1;
FILE * read2;
FILE * write1;
FILE * write2;

void process(int x) {

    if (!fork()) {
        if (!fork()) {
            if (!x) {
                fprintf(write1, "%lf\n", sin(x0));
                fflush(write1);

                for (int i = 1; i <= n; ++i) {
                    fprintf(write1, "%lf\n", x0);
                    fflush(write1);
                }


            } else {

            }
        }

        wait(NULL);
    }

    wait(NULL);
}

int main(int arg, char ** argv) {
    x0 = strtod(argv[1], NULL);
    dx = strtod(argv[3], NULL);
    atoi(argv[2]);

    pipe(fd1);
    pipe(fd2);

    read1 = fdopen(fd1[1]);
    write1 = fdopen(fd2[0]);
    read2 = fdopen(fd2[1]);
    write2 = fdopen(fd1[0]);

    process(0);
    process(1);
}