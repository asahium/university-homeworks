#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>

struct Node
{
    int32_t key;
    int32_t left_idx;
    int32_t right_idx;
};

int fd;

void traverse(int index) {
    struct Node result;

    lseek(fd, sizeof(result) * index, SEEK_SET);

    if (read(fd, &result, sizeof(result)) < sizeof(result))
        exit(0);

    if (result.right_idx)
        traverse(result.right_idx);

    printf("%d\n", result.key);

    if (result.left_idx)
        traverse(result.left_idx);
}

int main(int _, char ** argv) {
    fd = open(argv[1], O_RDONLY);
    traverse(0);
    close(fd);
}