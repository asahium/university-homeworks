#include <stdio.h>
#include <stdlib.h>

struct LLelem
{
    struct LLelem* next;
    int target;
};

struct LLelem* push(struct LLelem* target, int input) {
    struct LLelem* element = malloc(sizeof(struct LLelem));
    element->target = input;
    element->next = target;
    return element;
}

int main() {
    struct LLelem* list = NULL;
    int temp;

    while (scanf("%d", &temp) != EOF)
        list = push(list, temp);

    while (list != NULL) {
        printf("%d\n", list->target);
        struct LLelem* t_list = list->next;
        free(list);
        list = t_list;
    }

    return 0;
}
