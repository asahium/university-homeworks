#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    struct stat info;
    long long int size_sum = 0;
    for (int i = 1; i < argc; ++i) {
        int id = lstat(argv[i], &info);
        if ((id < 0) || (info.st_nlink != 1) ||
            !S_ISREG(info.st_mode) || S_ISLNK(info.st_mode)) {
            continue;
        }
        size_sum += info.st_size;
    }
    printf("%lld\n", size_sum);
}