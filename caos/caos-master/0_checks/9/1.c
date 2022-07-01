#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include <bits/sigthread.h>
#include <signal.h>
#include <stdio.h>
#include <bits/sigaction.h>
#include <signal.h>
#include <stdbool.h>

enum { N = 5 };

pthread_t ids[N];
pthread_t ids2[N];

void *func2(void *arg)
{
    pause();
    return NULL;
}

volatile int f = 0;

void *func(void *arg)
{
    int serial = (int) (intptr_t) arg;

    while (!f)
        continue;

    if (serial == 4)
        pthread_join(ids[3], NULL);

    if (serial == 1)
        pthread_join(ids[4], NULL);

    if (serial == 3)
        pthread_join(ids[0], NULL);

    if (serial == 0)
        pthread_join(ids[2], NULL);


    printf("%d\n", serial);

    return NULL;
}

int main()
{
    for (int i = 0; i < N; ++i) {
        pthread_create(&ids2[i], NULL, func2, NULL);
    }

    for (int i = 0; i < N; ++i) {
        pthread_create(&ids[i], NULL, func, (void*) (intptr_t) i);
    }

    for (int i = 0; i < N; ++i) {
        pthread_cancel(ids2[i]);
    }

    f = 1;
    pthread_join(ids[1], NULL);

    return 0;
}