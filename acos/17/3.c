#include <pthread.h>
#include <stdio.h>
#include <stdint.h>

enum {
    NUM = 3,
    OP_AMOUNT = 1000000
};

volatile double data[NUM];
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *thr_foo(void *ptr) {
    int ord = (int) (intptr_t) ptr;
    for (int i = 0; i < OP_AMOUNT; ++i) {
        pthread_mutex_lock(&mutex);
        data[ord] += (ord + 1) * 100;
        data[(ord + 1) % NUM] -= (ord + 1) * 100 + 1;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main(void) {
    pthread_t thrs[NUM];
    for (int i = 0; i < NUM; ++i) {
        pthread_create(thrs + i, NULL, thr_foo, (void *) (intptr_t) i);
    }
    for (int i = 0; i < NUM; ++i) {
        pthread_join(thrs[i], NULL);
    }
    for (int i = 0; i < NUM; ++i) {
        printf("%.10g\n", data[i]);
    }
}
