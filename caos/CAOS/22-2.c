/* Взято с семинара 194 группы */
#include <inttypes.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;


volatile int f = 0;
volatile uint64_t prime;


int is_prime(uint64_t cnt) {
    if (cnt < 2) {
        return 0;
    }
    for(uint64_t i = 2; i * i <= cnt; ++i) {
        if (cnt % i == 0) {
            return 0;
        }
    }
    return 1;
}


void * thread_func(void * ptr) {
    uint64_t base = *(uint64_t*) ptr;
    while(1) {
        if (is_prime(base)) {
            pthread_mutex_lock(&mut);
            prime = base;
            f = 1;
            pthread_cond_signal(&cond);
            pthread_mutex_unlock(&mut);
        }
        base += 1;
    }
    return NULL; 
}


int main(void) {
    uint64_t base;
    uint32_t count;
    scanf("%" SCNu64 "%" SCNu32, &base, &count); 
    pthread_t index;
    pthread_create(&index, NULL, thread_func, &base);
    for (uint32_t i = 0; i < count; ++i) {
        pthread_mutex_lock(&mut);
        while(!f) {
            pthread_cond_wait(&cond, &mut);
        }
        f = 0;
        uint64_t answer = prime;
        pthread_mutex_unlock(&mut);
        printf("%" PRIu64 "\n", answer);
    }
}

