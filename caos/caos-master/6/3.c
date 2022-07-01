#include <stdio.h>
#include <stdlib.h>

struct TI
{
    int n;
    struct TI *left;
    struct TI *right;
};

typedef struct TI TI;
typedef TI* TE;

TE root = NULL;

void print_and_free(TE r) {
    if (!r)
        return;

    print_and_free(r->right);
    printf("%d ", r->n);
    print_and_free(r->left);

    free(r);
}

void push(int n) {
    if (!root) {
        root = malloc(sizeof(TI));
        root->left = NULL;
        root->right = NULL;
        root->n = n;
        return;
    }

    TE it = root;
    TE item;

    while (1) {
        if (it->n == n)
            return;

        if (n < it->n) {
            if (it->left) {
                it = it->left;
            } else {
                item = malloc(sizeof(TI));
                item->left = NULL;
                item->right = NULL;
                item->n = n;
                it->left = item;
                return;
            }
        }

        if (n > it->n) {
            if (it->right) {
                it = it->right;
            } else {
                item = malloc(sizeof(TI));
                item->left = NULL;
                item->right = NULL;
                item->n = n;
                it->right = item;
                return;
            }
        }
    }
}

int main() {
    int n;
    int s = 0;

    while (scanf("%d", &n) != EOF) {
        if (!n) {
            print_and_free(root);
            printf("0 ");
            root = NULL;
            s = 0;
            continue;
        }

        push(n);
        s = 1;
    }

    if (s) {
        print_and_free(root);
        printf("0");
    }

    printf("\n");
}

