#include <pthread.h>
#include <stdatomic.h>
#include <sched.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

struct Item {
    struct Item *next;
    long long value;
};

struct Item * _Atomic head = NULL;

enum {
    THREAD_AM = 100,
    THREAD_ELEMS = 1000
};

void * thread_func(void *arg) {
    int ind = (int) (intptr_t) arg;
    for (int i = 0; i != THREAD_ELEMS; ++i) {
        struct Item *new_item = calloc(1, sizeof(*new_item));
        new_item->value = ind * THREAD_ELEMS + i;
        new_item->next = atomic_exchange_explicit(&head, new_item, memory_order_relaxed);
        sched_yield();
    }
    return NULL;
}

int main(void) {
    pthread_t threads[THREAD_AM];
    pthread_attr_t attr;
    pthread_attr_init(&attr);                                                   
    pthread_attr_setstacksize(&attr, sysconf(_SC_THREAD_STACK_MIN));
    pthread_attr_setguardsize(&attr, 0); 
    for (int i = 0; i < THREAD_AM; ++i) {
        pthread_create(threads + i, &attr, thread_func, (void *) (intptr_t) i);
    }
    for (int i = 0; i < THREAD_AM; ++i) {
        pthread_join(threads[i], NULL);
    }
    for (struct Item *cur = head; cur != NULL; cur = cur->next) {
        printf("%lld\n", cur->value);
    }
    return 0;
}

