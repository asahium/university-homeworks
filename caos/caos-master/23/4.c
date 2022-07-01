#include <pthread.h>
#include <sched.h>
#include <stdint.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define pt(x) p##thread_mutex_##x

struct Elem
{
    int it;

    uint32_t indx1;
    uint32_t indx2;

    double sum1;
    double sum2;
    double * accounts;

    pthread_mutex_t * mutexes;
};

typedef struct Elem Elem;

void * process(void *ptr) {
    Elem * item = (Elem *) ptr;

    for (int i = 0; i < item->it; ++i) {
        pt(lock(&item->mutexes[item->indx1]));
        pt(lock(&item->mutexes[item->indx2]));

        item->accounts[item->indx1] += item->sum1;
        item->accounts[item->indx2] += item->sum2;

        pt(unlock(&item->mutexes[item->indx2]));
        pt(unlock(&item->mutexes[item->indx1]));
    }

    return NULL;
}

int main() {
    uint32_t count, threads;

    scanf("%u %u", &count, &threads);

    pthread_t * ids = malloc(threads * sizeof(pthread_t));
    Elem * elems = malloc(threads * sizeof(Elem));

    double * accounts = malloc(count * sizeof(double));
    pt(t) * mutexes = malloc(count * sizeof(pt(t)));

    for (int i = 0; i < count; ++i) {
        pt(init(&mutexes[i], NULL));
        accounts[i] = 0;
    }

    pthread_attr_t pa;
    pthread_attr_init(&pa);
    pthread_attr_setstacksize(&pa, sysconf(_SC_THREAD_STACK_MIN));

    for (int i = 0; i < threads; ++i) {
        scanf("%u %u %lg %u %lg",  &elems[i].it, &elems[i].indx1,
                &elems[i].sum1, &elems[i].indx2, &elems[i].sum2);

        if (elems[i].indx1 > elems[i].indx2) {
            uint32_t tt = elems[i].indx1;
            elems[i].indx1 = elems[i].indx2;
            elems[i].indx2 = tt;

            double t = elems[i].sum1;
            elems[i].sum1 = elems[i].sum2;
            elems[i].sum2 = t;
        }

        elems[i].mutexes = mutexes;
        elems[i].accounts = accounts;

        pthread_create(&ids[i], &pa, process, &elems[i]);
    }

    pthread_attr_destroy(&pa);

    for (int i = 0; i < threads; ++i)
        pthread_join(ids[i], NULL);

    for (int i = 0; i < count; ++i)
        printf("%.10g\n", accounts[i]);

    free(ids);
    free(accounts);
    free(elems);
    free(mutexes);
}
