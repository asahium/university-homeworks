#include <sys/stat.h>
#include <stdlib.h>
#include <stdio.h>


int main(int argc, char* argv[]) {
    struct stat file;
    long long total = 0;
    
    for (int i = 1; i < argc; ++i) {
        if (lstat(argv[i], &file) == 0 && S_ISREG(file.st_mode) && file.st_nlink == 1) {
            total += file.st_size;
        }
    }
    printf("%lld\n", total);
}

