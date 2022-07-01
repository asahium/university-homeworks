#include <pthread.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

// In fact, const or static const doesn't mean constness,
// as well as using macros, so only enum values here are allowed
enum { SIZE = 3, COUNT = 1000000 };

volatile double result[SIZE];

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void * process(void *ptr) {
    int index = (int) (intptr_t) ptr;

    for (int i = 0; i < COUNT; ++i) {
        pthread_mutex_lock(&mutex);

        if (!index) {
            result[0] += 100;
            result[1] -= 101;
        } else if (index == 1) {
            result[1] += 200;
            result[2] -= 201;
        } else {
            result[2] += 300;
            result[0] -= 301;
        }

        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

int main() {
    pthread_t ids[SIZE];

    for (int i = 0; i < SIZE; ++i)
        pthread_create(&ids[i], NULL, process, (void *) (intptr_t) i);

    for (int i = 0; i < SIZE; ++i)
        pthread_join(ids[i], NULL);

    printf("%.10g %.10g %.10g\n", result[0], result[1], result[2]);
}
