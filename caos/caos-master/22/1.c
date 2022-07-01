#include <stdio.h>
#include <sys/types.h>
#include <pthread.h>

typedef struct Params
{
    int id;
    pthread_t prev;
} P;

void * handler(void * ptr) {
    P params = *(P *)(ptr);

    if (params.id > 0)
        pthread_join(params.prev, NULL);

    printf("%d\n", params.id);
    fflush(stdout);

    return NULL;
}

int main() {
    P threads[10];

    pthread_t thread = 0;

    for (int i = 0; i < 10; ++i) {
        threads[i].id = i;
        threads[i].prev = thread;
        pthread_create(&thread, NULL, handler, &threads[i]);
    }

    pthread_join(thread, NULL);
}