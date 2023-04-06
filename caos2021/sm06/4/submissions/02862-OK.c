#include <stdio.h>
#include <stdlib.h>

typedef struct Item {
    int val;
    struct Item *next;
} Item;

int main(void) {
    int input;
    Item* header = NULL;
    while (scanf("%d", &input) == 1) {
        Item* it = calloc(1, sizeof(*it));
        if (!it) {
            free(header);
            fprintf(stderr, "error in calloc");
            return 1;
        }
        it->val = input;
        it->next = header;
        header = it;
    }
    while (header) {
        printf("%d\n", header->val);
        Item* it = header;
        header = header->next;
        free(it);
    }
    return 0;
}
