#include <malloc.h>

void destroy(void *rr) {
    free(rr);
}

int next(void *rr);

typedef struct
{
    void (*destroy)(void*);
    int (*next)(void*);
} Op;

typedef struct
{
    Op *ops;
    int seed;
} RandomGenerator;

int next(void *rr) {
    RandomGenerator* rg = rr;
    int next = (rg->seed * 1103515245u + 12345) % (1u << 31);
    rg->seed = next;
    return next;
}

const Op op = (Op) { &destroy, &next };

RandomGenerator *random_create(int seed) {
    RandomGenerator *rr = malloc(sizeof(RandomGenerator));
    rr->seed = seed;
    rr->ops = (Op*)&op;
    return rr;
}
