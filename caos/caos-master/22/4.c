#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

pthread_t * ids;
int * fds;
int N;

void * thread_func(void * ptr) {
    int n = *((intptr_t *) ptr);
    int t = 0;
    int next = 0;

    while (1) {
        read(fds[2 * n], &t, sizeof(t));

        if (scanf("%d", &next) == 1) {
            printf("%d %d\n", n, next);
            fflush(stdout);

            next %= N;
            next += next < 0 ? N : 0;

            write(fds[2 * next + 1], &next, sizeof(next));
            fflush(stdout);
        } else {
            next = (n + 1) % N;
            write(fds[2 * next + 1], &next, sizeof(next));
            fflush(stdout);
            break;
        }
    }

    return NULL;
}

int main(int argc, char ** argv) {
    N = strtol(argv[1], NULL, 10);

    pthread_t ids_a[N];
    int fds_a[2 * N];

    ids = ids_a;
    fds = fds_a;

    int pids[N];

    for (int i = 0; i < N; ++i) {
        pids[i] = i;
        pipe(&(fds[2 * i]));
    }

    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setstacksize(&attr, sysconf(_SC_THREAD_STACK_MIN));

    for (int i = 0; i < N; ++i)
        pthread_create(&ids[i], &attr, thread_func, &pids[i]);

    int t = 0;
    write(fds[1], &t, sizeof(t));

    for (int i = 0; i < N; ++i)
        pthread_join(ids[i], NULL);

    for (int i = 0; i < N; ++i) {
        close(fds[2 * i]);
        close(fds[2 * i + 1]);
    }

    pthread_attr_destroy(&attr);
}