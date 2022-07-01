#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>

struct Node {
    int32_t key;
    int32_t left_idx;
    int32_t right_idx;
};

int file;

void dec_order_print(int index) {
    struct Node node;

    lseek(file, sizeof(node) * index, SEEK_SET);

    if (read(file, &node, sizeof(node)) < sizeof(node)) {
        exit(0);
    }

    if (node.right_idx){
        dec_order_print(node.right_idx);
    }

    printf("%d\n", node.key);

    if (node.left_idx) {
        dec_order_print(node.left_idx);
    }
}

int main(int argc, char** argv) {
    file = open(argv[1], O_RDONLY);
    dec_order_print(0);
    close(file);
}