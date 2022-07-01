/* Взято с семинара 194 группы */
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void * thr_foo(void *arg) {
    long long partial = 0;
    int input;
    while (scanf("%d", &input) == 1) {
        partial += input;
        sched_yield();
    }
    *(long long *) arg = partial;
    return NULL;
}

int main(int argc, char **argv) {
    int n = strtol(argv[1], NULL, 10);
    pthread_t *thrs = calloc(n, sizeof(*thrs));
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setstacksize(&attr, sysconf(_SC_THREAD_STACK_MIN));
    pthread_attr_setguardsize(&attr, 0);
    long long sum = 0;
    long long *partials = calloc(n, sizeof(*partials));
    for (int i = 0; i < n; ++i) {
        pthread_create(thrs + i, &attr, thr_foo, partials + i);
    }
    pthread_attr_destroy(&attr);
    for (int i = 0; i < n; ++i) {
        pthread_join(thrs[i], NULL);
        sum += partials[i];
    }
    printf("%lld\n", sum);
}