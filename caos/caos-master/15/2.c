#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <memory.h>

void write_matrix(int32_t *data, int rows, int cols) {
    int32_t i = 1;

    int min_col = 0, min_row = 0;
    int max_col = cols, max_row = rows;

    while (min_col < max_col && min_row < max_row) {
        for (int h = min_col; h < max_col; ++h)
            data[min_row * cols + h] = i++;

        if (++min_row >= max_row)
            break;

        for (int v = min_row; v < max_row; ++v)
            data[v * cols + (max_col - 1)] = i++;

        if (--max_col <= min_col)
            break;

        for (int h = max_col; h > min_col; --h)
            data[(max_row - 1) * cols + h - 1] = i++;

        if (--max_row <= min_row)
            break;

        for (int v = max_row - 1; v > min_row - 1; --v)
            data[v * cols + min_col] = i++;

        ++min_col;
    }
}

int main(int argc, char ** argv) {
    int rows = atoi(argv[2]);
    int cols = atoi(argv[3]);
    int64_t size = rows * cols * sizeof(int32_t);

    int fd = open(argv[1], O_RDWR | O_CREAT | O_TRUNC, 0644);

    ftruncate(fd, size);

    int32_t * matrix = mmap(NULL, size, PROT_WRITE, MAP_SHARED, fd, 0);

    write_matrix(matrix, rows, cols);

    munmap(matrix, size);

    close(fd);
}
