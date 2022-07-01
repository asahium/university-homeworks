#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <dirent.h>
#include <limits.h>
#include <unistd.h>
#include <ctype.h>

int main(int argc, char* argv[]) {
    DIR * dir = opendir(argv[1]);

    if (!dir) {
        printf("0\n");
        return 0;
    }

    struct dirent *entry = readdir(dir);

    unsigned long long size = 0;

    uid_t uid = getuid();

    while (entry) {
        char buf[PATH_MAX + 1];

        snprintf(buf, PATH_MAX, "%s/%s", argv[1], entry->d_name);

        struct stat file_stat;

        if (stat(buf, &file_stat) == 0 &&
            S_ISREG(file_stat.st_mode) &&
            file_stat.st_uid == uid &&
            isupper(entry->d_name[0])) {

            size += file_stat.st_size;
        }

        entry = readdir(dir);
    }

    printf("%llu\n", size);

    closedir(dir);
}
