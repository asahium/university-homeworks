#include <stdio.h>
#include <sys/types.h>
#include <pthread.h>

void * handler(void * _) {
    (void)_;

    int n;

    if (scanf("%d", &n) == 1) {
        pthread_t thread;
        pthread_create(&thread, NULL, handler, NULL);
        pthread_join(thread, NULL);
        printf("%d\n", n);
    }

    return NULL;
}

int main() {
    pthread_t thread;
    pthread_create(&thread, NULL, handler, NULL);
    pthread_join(thread, NULL);
}
