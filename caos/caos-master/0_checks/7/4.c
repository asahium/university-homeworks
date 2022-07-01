#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <wait.h>
#include <inttypes.h>

int main(int argc, char ** argv) {
    int left[2], right[2];
    pipe(left);
    pipe(right);

    FILE * l_read = fdopen(left[0], "r");
    FILE * l_write = fdopen(left[1], "w");
    FILE * r_read = fdopen(right[0], "r");
    FILE * r_write = fdopen(right[1], "w");
    FILE * file1 = fopen(argv[1], "r");
    FILE * file2 = fopen(argv[2], "r");

    pid_t pid = fork();

    if (!pid) {
        fclose(r_write);
        fclose(l_read);
        fclose(file2);
        fclose(r_read);

        int score;
        unsigned long long result = 0;

        while (fscanf(file1, "%d", &score) == 1)
            result += score;

        fprintf(l_write, "%d\n", (int)result);
        fflush(l_write);

        fclose(l_write);
        fclose(file1);

        exit(0);
    } else {
        pid_t pid2 = fork();

        if (!pid2) {
            fclose(l_write);
            fclose(r_read);
            fclose(l_read);
            fclose(file1);

            int score;
            unsigned long long result = 0;

            while (fscanf(file2, "%d", &score) == 1)
                result += score;

            fprintf(r_write, "%d\n", (int) result);
            fflush(r_write);

            fclose(r_write);
            fclose(file2);

            exit(0);
        } else {
            fclose(file1);
            fclose(file2);
            fclose(r_write);
            fclose(l_write);

            int f1s, f2s;

            waitpid(pid2, NULL, 0);

            fscanf(r_read, "%d", &f2s);
            fclose(r_read);

            waitpid(pid, NULL, 0);

            fscanf(l_read, "%d", &f1s);
            fclose(l_read);


            int32_t out = (int64_t)f1s + f2s;

            printf("%d %d %" PRId32, f2s, f1s, out);
            fflush(stdout);
        }
    }
}