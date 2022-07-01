#include <stdio.h>
#include <stdlib.h>

struct LL
{
    struct LL* prev;
    struct LL* next;
    int num;
    long long count;
};

typedef struct LL * LLP;

LLP head = NULL;
LLP last = NULL;

void push(int input) {
    for (LLP it = head; it != NULL; it = it->next) {
        if (it->num != input)
            continue;

        if (it == head) {
            ++it->count;
            return;
        }

        LLP prev = it->prev;
        LLP next = it->next;

        if (prev)
            prev->next = next;

        next ? (next->prev = prev) : (last = it->prev);

        it->prev = NULL;
        it->next = head;
        head->prev = it;

        ++it->count;

        head = it;

        return;
    }

    if (!head) {
        head = malloc(sizeof(struct LL));
        head->num = input;
        head->count = 1;
        head->next = NULL;
        head->prev = NULL;

        last = head;

        return;
    }

    LLP element = malloc(sizeof(struct LL));
    element->prev = NULL;
    element->next = head;
    head->prev = element;

    element->num = input;
    element->count = 1;

    head = element;
}

int main() {
    int temp;

    while (scanf("%d", &temp) == 1)
        push(temp);

    while (last) {
        printf("%d %lld\n", last->num, last->count);

        LLP t = last->prev;
        free(last);
        last = t;
    }

    return 0;
}