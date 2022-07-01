#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int prime(uint64_t n) {
    if (n < 3)
        return n == 2;

    for (uint64_t i = 2; i * i <= n; ++i)
        if (!(n % i))
            return 0;

    return 1;
}

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t condvar = PTHREAD_COND_INITIALIZER;

volatile int state = 0;
uint64_t current = 0;

void *process(void *ptr) {
    uint64_t *base = ptr;

    while (1) {

        if (!prime(*base)) {
            ++*base;
            continue;
        }

        pthread_mutex_lock(&mutex);
        state = 1;
        current = (*base)++;
        pthread_cond_signal(&condvar);
        pthread_mutex_unlock(&mutex);
    }
}

int main() {
    uint64_t base;
    uint32_t count;

    scanf("%" SCNu64 "%" SCNu32, &base, &count);

    pthread_t id;

    pthread_create(&id, NULL, process, &base);

    for (uint32_t i = 0; i < count; ++i) {
        pthread_mutex_lock(&mutex);

        if (!state)
            pthread_cond_wait(&condvar, &mutex);

        pthread_mutex_unlock(&mutex);

        printf("%" PRIu64 "\n", current);

        state = 0;
    }
}
