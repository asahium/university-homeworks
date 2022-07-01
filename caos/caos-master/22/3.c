#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <sched.h>
#include <unistd.h>

void * thread_func(void *ptr) {
    int n;
    long long * sum = ptr;

    *sum = 0;

    while (scanf("%d", &n) == 1) {
        *sum += n;
        sched_yield();
    }

    return NULL;
}

int main(int argc, char **argv) {
    int n = atoi(argv[1]);

    pthread_t ids[n];
    long long partial[n];

    pthread_attr_t pa;
    pthread_attr_init(&pa);
    pthread_attr_setstacksize(&pa, sysconf(_SC_THREAD_STACK_MIN));

    for (int i = 0; i < n; ++i)
        pthread_create(&ids[i], &pa, thread_func, partial + i);

    pthread_attr_destroy(&pa);

    long long res = 0;

    for (int i = 0; i < n; ++i) {
        pthread_join(ids[i], NULL);
        res += partial[i];
    }

    printf("%lld\n", res);
    fflush(stdout);
}