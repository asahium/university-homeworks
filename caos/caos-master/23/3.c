#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct Item
{
    struct Item *next;
    long long value;
};

typedef struct Item Item;

Item * _Atomic root = NULL;

void * process(void * ptr) {
    long start = (long) ptr;

    for (int i = 0; i < 1000; ++i) {
        Item * t = malloc(sizeof(Item));

        t->next = atomic_exchange(&root, t);
        t->value = start + i;

        sched_yield();
    }

    return NULL;
}

int main() {
    pthread_t ids[100];

    pthread_attr_t pa;
    pthread_attr_init(&pa);
    pthread_attr_setstacksize(&pa, sysconf(_SC_THREAD_STACK_MIN));

    for (int i = 0; i < 100; ++i)
        pthread_create(&ids[i], &pa, process, (void *) ((long) i * 1000));

    pthread_attr_destroy(&pa);

    for (int i = 0; i < 100; ++i)
        pthread_join(ids[i], NULL);

    Item * t;
    while (root) {
        t = root;
        printf("%lld\n", root->value);
        root = root->next;
        free(t);
    }
}
