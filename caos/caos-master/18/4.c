#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <wait.h>

int main(int argc, char ** argv) {
    int left[2], right[2];

    long long desired = strtoll(argv[1], NULL, 0);

    if (desired < 2) {
        printf("Done");
        return 0;
    }

    pipe(left);
    pipe(right);

    FILE * l_read = fdopen(left[0], "r");
    FILE * l_write = fdopen(left[1], "w");
    FILE * r_read = fdopen(right[0], "r");
    FILE * r_write = fdopen(right[1], "w");

    pid_t pid = fork();

    if (!pid) {
        fclose(r_write);
        fclose(l_read);

        long long score;

        while (fscanf(r_read, "%lld", &score) != EOF && score != desired) {
            printf("1 %lld\n", score);

            fprintf(l_write, "%lld\n", ++score);

            fflush(l_write);
            fflush(stdout);
        }

        fclose(l_write);
        fclose(r_read);

        exit(0);
    } else {
        pid = fork();

        if (!pid) {
            fclose(l_write);
            fclose(r_read);

            fprintf(r_write, "1\n");
            fflush(r_write);

            long long score;

            while (fscanf(l_read, "%lld", &score) != EOF && score != desired) {
                printf("2 %lld\n", score);
                fprintf(r_write, "%lld\n", ++score);

                fflush(r_write);
                fflush(stdout);
            }

            fclose(r_write);
            fclose(l_read);

            exit(0);
        } else {
            fclose(r_write);
            fclose(r_read);
            fclose(l_write);
            fclose(l_read);

            int s;
            while ((wait(&s)) > 0);

            printf("Done");
            fflush(stdout);
        }
    }
}