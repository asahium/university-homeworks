#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
    long long count = 0;
    struct stat str;

    for (int i = 1; i < argc; ++i) {
        int id = lstat(argv[i], &str);

        if (id < 0)
            continue;

        if (!S_ISREG(str.st_mode) || S_ISLNK(str.st_mode))
            continue;

        if (str.st_nlink != 1)
            continue;

        count += str.st_size;
    }

    printf("%llu\n", count);
}
