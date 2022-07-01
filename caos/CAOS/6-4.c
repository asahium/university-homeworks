#include <malloc.h>
#include <stdlib.h>

enum {
    MUL = 1103515245,
    INC = 12345,
    MOD = 31
};

int next(void *rr);

void destroy(void *rr) {
    free(rr);
}

typedef struct {
    void (*destroy)(void*);
    int (*next)(void*);
} funcs;

typedef struct {
    funcs *ops;
    int seed;
} RandomGenerator;

int next(void *rr) {
    RandomGenerator* rg = rr;
    int next = (rg->seed * (long long)MUL + INC) % (1u << MOD);
    rg->seed = next;
    return next;
}

const funcs fpointer = (funcs) { &destroy, &next };

RandomGenerator *random_create(int seed) {
    RandomGenerator *rr = calloc(1, sizeof(RandomGenerator));
    if (!rr) {
        free(rr);
        fprintf(stderr, "error in calloc");
        return NULL;
    }
    rr->seed = seed;
    rr->ops = (funcs*)&fpointer;
    return rr;
}