/* Взято с семинара 194 группы */
#include <stdio.h>
#include <stdint.h>
#include <pthread.h>

enum{
    N_THREAD = 10
};

pthread_t threads[N_THREAD];

void * thread_template(void *ptr) {
    int idx = (int) (intptr_t) ptr;
    if (idx) {
        pthread_join(threads[idx - 1], NULL);
    }
    printf("%d\n", idx);
    fflush(stdout);
    return NULL;
}

int main(void) {
    for (int i = 0; i < N_THREAD; ++i) {
        pthread_create(threads + i, NULL,
                       thread_template,
                       (void *) (intptr_t) i);
    }
    pthread_join(threads[N_THREAD - 1], NULL);
    return 0;
}
