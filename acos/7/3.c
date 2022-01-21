#include <stdio.h>
#include <stdlib.h>

struct Node {
    struct Node* left;
    struct Node* right;
    int value;
};

typedef struct Node Node;
typedef Node * tree;

tree root = NULL;

void add(int input) {
    if (!root) {
        root = malloc(sizeof(Node));
        if (!root) {
            free(root);
            fprintf(stderr, "error in malloc");
            return;
        }
        root->left = NULL;
        root->right = NULL;
        root->value = input;
        return;
    }
    tree it = root;
    while (1) {
        if (it->value == input) {
            return;
        }
        if (input < it->value) {
            if (it->left) {
                it = it->left;
            } else {
                tree item = malloc(sizeof(Node));
                if (!item) {
                    free(item);
                    fprintf(stderr, "error in malloc");
                    return;
                }
                item->left = NULL;
                item->right = NULL;
                item->value = input;
                it->left = item;
                return;
            }
        } else {
            if (it->right) {
                it = it->right;
            } else {
                tree item = malloc(sizeof(Node));
                if (!item) {
                    free(item);
                    fprintf(stderr, "error in calloc");
                    return;
                }
                item->left = NULL;
                item->right = NULL;
                item->value = input;
                it->right = item;
                return;
            }
        }
    }
}

void print_tree(tree Node) {
    if (!Node) {
        return;
    }
    print_tree(Node->right);
    printf("%d ", Node->value);
    print_tree(Node->left);
    free(Node);
}

int main(void) {
    int input, checker = 0;
    while (scanf("%d", &input) != EOF) {
        if (input == 0) {
            checker = 0;
            print_tree(root);
            printf("0 ");
            root = NULL;
            continue;
        }
        add(input);
        checker = 1;
    }
    if (checker) {
        print_tree(root);
        printf("0");
    }
    printf("\n");
}
