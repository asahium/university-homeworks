#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int my_argc;
char **my_argv;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t *condvar;

void *thread_func(void *ptr) {
    int num = (int)(intptr_t) ptr;
    FILE *f = fopen(my_argv[num], "r");
    uint64_t a, b, n, result;
    pthread_t id;
    if (fscanf(f, "%llu%llu%llu", &a, &b, &n) == 3) {
        ++num;
        pthread_create(&id, NULL, thread_func, (void *)(intptr_t)num);
        --num;
        result = (a + b) % n;
        if (result < a || result < b) {
            result += ((~(uint64_t)0) % n + 1) % n;
            result %= n;
        }
    }
    pthread_mutex_lock(&m);
    while (num != my_argc) {
        pthread_cond_wait(&condvar[num], &m);
    }
    --my_argc;
    pthread_mutex_unlock(&m);
    printf("%llu\n", result);

    fflush(stdout);
    fclose(f);
    return NULL;
}

int main(int argc, char **argv) {
    condvar = malloc((argc - 1) * sizeof(pthread_cond_t));
    pthread_t *ids = malloc((argc - 1) * sizeof(pthread_t));
    for (uint32_t i = 0; i < argc - 1; ++i) {
        pthread_cond_init(&condvar[i], NULL);
    }
    pthread_attr_t pa;
    pthread_attr_init(&pa);
    pthread_attr_setstacksize(&pa, sysconf(_SC_THREAD_STACK_MIN));
    my_argc = argc - 1;
    my_argv = argv;
    for (int i = 0; i < my_argc; ++i) {
        pthread_create(&ids[i], &pa, thread_func, (void*)(intptr_t)i);
    }
    pthread_attr_destroy(&pa);
    for (int i = 0; i < my_argc; ++i) {
        pthread_join(ids[i], NULL);
    }
    free(condvar);
    free(ids);
}