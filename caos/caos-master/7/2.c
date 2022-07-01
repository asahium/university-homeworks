#include <stdlib.h>

static int compare(const void *p1, const void *p2, void* d) {
    int a = *(int *)p1;
    int b = *(int *)p2;
    int* data = (int *) d;

    if (data[a] > data[b]) {
        return 1;
    } else if (data[a] == data[b]) {
        return a < b ? -1 : a != b;
    }

    return -1;
}


void process(size_t count, const int *data, int *order) {
    for (size_t i = 0; i < count; ++i)
        order[i] = i;

    qsort_r(order, count, sizeof(int), compare, (void *)data);
}
