#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

pthread_mutex_t ** mutexes;

typedef struct STR
{
    int i, r, c, in;
} ST;


int cols, rows, increments;

int** matrices;

void * process(void * p) {

    ST cu = *(ST*) p;

    if (cu.c == -1) {

        for (int i = 0; i < cu.i; ++i) {
            for (int j = 0; j < cols; ++j) {
                pthread_mutex_lock(&mutexes[cu.r][j]);

                matrices[cu.r][j] += cu.in;

                pthread_mutex_unlock(&mutexes[cu.r][j]);
            }
        }

    } else if (cu.r == -1) {
        for (int i = 0; i < cu.i; ++i) {
            for (int j = 0; j < rows; ++j) {

                pthread_mutex_unlock(&mutexes[j][cu.c]);

                matrices[j][cu.c] += cu.in;

                pthread_mutex_unlock(&mutexes[j][cu.c]);

            }
        }
    }

    return NULL;

}

int main() {

    pthread_attr_t pa;
    pthread_attr_init(&pa);
    pthread_attr_setstacksize(&pa, sysconf(_SC_THREAD_STACK_MIN));


    scanf("%d %d %d", &rows, &cols, &increments);

    matrices = calloc(rows, sizeof(*matrices));
    mutexes = calloc(rows, sizeof(*mutexes));

    for (int i = 0; i < rows; ++i) {
        mutexes[i] = calloc(rows, sizeof(*mutexes[i]));
        matrices[i] = calloc(cols, sizeof(*mutexes[i]));

        for (int j = 0; j < cols; ++j)
            pthread_mutex_init(&mutexes[i][j], NULL);
    }

    ST arg[increments];
    pthread_t ids[increments];

    for (int i = 0; i != increments; ++i) {
        scanf("%d %d %d %d", &arg[i].i, &arg[i].r, &arg[i].c, &arg[i].in);

        pthread_create(&ids[i], &pa, process, (void *) &arg[i]);
    }

    pthread_attr_destroy(&pa);

    for (int i = 0; i < increments; ++i)
        pthread_join(ids[i], NULL);

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j)
            printf("%d ", matrices[i][j]);
        printf("\n");
    }

    for (int i = 0; i < rows; ++i) {
        free(matrices[i]);
        free(mutexes[i]);
    }

    free(matrices);
    free(mutexes);
}