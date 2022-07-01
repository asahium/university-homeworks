#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/stat.h>

char * path;
long start, end;

int fd;

off_t size;

char * mapped;

long newlines_count;

void h_argc(int argc) {
    if (argc != 4) {
        fprintf(stderr, "invalid arguments count\n");
        exit(1);
    }
}

void h_argv(char **argv) {
    errno = 0;

    path = argv[1];

    char * e;

    start = strtol(argv[2], &e, 0);

    if (*e || errno) {
        fprintf(stderr, "line arguments error\n");
        exit(1);
    }

    end = strtol(argv[3], &e, 0);

    if (*e || errno) {
        fprintf(stderr, "line arguments error\n");
        exit(1);
    }
}

int h_line_args() {
    if (start <= 0 || end <= 0) {
        fprintf(stderr, "line arguments should be positive numbers\n");
        exit(1);
    }

    return start >= end;
}

void h_fd() {
    fd = open(path, O_RDONLY);

    if (fd < 0) {
        fprintf(stderr, "Cannot open file\n");
        exit(1);
    }

    struct stat finfo;
    if (fstat(fd, &finfo) == -1) {
        fprintf(stderr, "File info retrieve error\n");
        exit(1);
    }

    if (!S_ISREG(finfo.st_mode)) {
        fprintf(stderr, "File info retrieve error\n");
        exit(1);
    }
}

int h_size() {
    size = lseek(fd, 0, SEEK_END);

    if (size == -1) {
        close(fd);
        fprintf(stderr, "Error in lseek\n");
        exit(1);
    }

    if (!size) {
        close(fd);
        return 1;
    }

    return 0;
}

void h_mmap() {
    mapped = (char *) mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);

    if (mapped == MAP_FAILED) {
        close(fd);
        fprintf(stderr, "Error in mmap\n");
        exit(1);
    }
}

void h_newlines() {
    newlines_count = 0;

    for (long i = 0; i < size; ++i)
        if (mapped[i] == '\n')
            ++newlines_count;
}

void h_newline_indx(long * newline_indexes){
    newline_indexes[0] = -1;
    newline_indexes[newlines_count + 1] = size + 2;

    int indx = 0;

    for (long i = 0; i < size; ++i)
        if (mapped[i] == '\n')
            newline_indexes[++indx] = i;
}

int h_bounds() {
    if (start > newlines_count + 1) {
        munmap(mapped, size);
        close(fd);

        fprintf(stderr, "Error in mmap\n");
        exit(1);
    }

    --start;
    --end;

    if (end > newlines_count)
        end = newlines_count;

    return 0;
}

void print_line(long i_start, long i_end) {
    for (long i = i_start + 1; i < i_end; ++i)
        printf("%c", mapped[i]);
}

int main(int argc, char ** argv) {
    h_argc(argc);
    h_argv(argv);
    h_fd();

    if (h_line_args())
        return 0;

    if (h_size())
        return 0;

    h_mmap();
    h_newlines();

    long newline_indexes[newlines_count + 2];
    h_newline_indx(newline_indexes);

    if (h_bounds())
        return 0;

    for (long i = end; i > start; --i) {
        print_line(newline_indexes[i - 1], newline_indexes[i]);
        printf("\n");
    }

    munmap(mapped, size);
    close(fd);
}