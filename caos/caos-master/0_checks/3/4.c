#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct Elem
{
    struct Elem *next;
    char *str;
};

int correct(struct Elem *item, int32_t *value) {
    char *p;
    errno = 0;

    int64_t t = strtol(item->str, &p, 0);

    if (!*(item->str) || *p || errno || (t - (int32_t)t))
        return 0;

    *value = t;

    return 1;
}

struct Elem * dup_elem(struct Elem * head) {
    if (!head)
        return head;

    struct Elem * prev = NULL;

    for (struct Elem * current = head; !!current; prev = current, current = current->next) {
        int32_t value;

        if (!correct(current, &value) || value == (~(~0u >> 1)))
            continue;

        struct Elem *n = malloc(sizeof(struct Elem));

        if (!prev)
            head = n;
        else
            prev->next = n;

        n->next = current;
        n->str = malloc(13 * sizeof(char));

        sprintf(n->str, "%d", value - 1);
    }

    return head;
}
