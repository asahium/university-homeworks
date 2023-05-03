#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <memory.h>

void spiralize(int32_t *data, int rows, int cols) {
    int32_t i = 1;
    int min_col = 0, min_row = 0;
    int max_col = cols, max_row = rows;
    while ((min_col < max_col) && (min_row < max_row)) {
        for (int j = min_col; j < max_col; ++j){
            data[min_row * cols + j] = i++;
        }
        if (++min_row >= max_row) {
            break;
        }
        for (int j = min_row; j < max_row; ++j) {
            data[j * cols + (max_col - 1)] = i++;
        }
        if (--max_col <= min_col) {
            break;
        }
        for (int j = max_col; j > min_col; --j) {
            data[(max_row - 1) * cols + j - 1] = i++;
        }
        if (--max_row <= min_row) {
            break;
        }
        for (int j = max_row - 1; j > min_row - 1; --j) {
            data[j * cols + min_col] = i++;
        }
        ++min_col;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        exit(1);
    }
    int rows = atoi(argv[2]);
    int cols = atoi(argv[3]);
    int64_t size = rows * cols * sizeof(int32_t);
    int file = open(argv[1], O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (file < 0) {
        exit(1);
    }
    int32_t* matrix = mmap(NULL, size, PROT_WRITE, MAP_SHARED, file, 0);
    if (ftruncate(file, size) == -1) {
        close(file);
        return 1;
    }
    if  (matrix == MAP_FAILED) {
        close(file);
        return 1;
    }
    spiralize(matrix, rows, cols);
    munmap(matrix, size);
    close(file);
    return 0;
}
