#include <stdio.h>
#include <stdlib.h>

struct List {
    struct List *left;
    struct List *right;
    int x;
    long long count;
};

typedef struct List *mylist;

mylist head = NULL;
mylist last = NULL;

void add(int input) {
    if (!head) {
        head = malloc(sizeof(struct List));
        head->left = NULL;
        head->right = NULL;
        head->x = input;
        head->count =  1;
        last = head;
        return;
    }
    mylist it = head;
    if (head->x == input) {
        head->count = head->count + 1;
        return;
    }
    while (it != NULL) {
        if (it->x == input) {
            mylist left = it->left;
            mylist right = it->right;
            left->right = right;
            if (right) {
                right->left = left;
            } else {
                last = it->left;
            }
            it->left = NULL;
            it->right = head;
            head->left = it;
            it->count = it->count + 1;
            head = it;
            return;
        }
        it = it->right;
    }
    mylist newhead = malloc(sizeof(struct List));
    if (!newhead) {
        while (last) {
            mylist t = last->left;
            free(last);
            last = t;
        }
        fprintf(stderr, "error in malloc");
        return;
    }
    newhead->left = NULL;
    newhead->right = head;
    head->left = newhead;
    newhead->x = input;
    newhead->count = 1;
    head = newhead;
    return;
}
    
int main(void) {
    int input;
    while (scanf("%d", &input) == 1) {
        add(input);
    }
    while (last) {
        printf("%d %lld\n", last->x, last->count);
        mylist t = last->left;
        free(last);
        last = t;
    }
    return 0;
}
