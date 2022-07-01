#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <dirent.h>
#include <limits.h>
#include <unistd.h>
#include <ctype.h>

int main(int argc, char* argv[]) {
    unsigned long long size = 0;
    DIR * dir = opendir(argv[1]);
    if (!dir) {
        printf("%llu\n", size);
        return 0;
    }
    struct dirent *content = readdir(dir);
    uid_t uid = getuid();
    while (content) {
        char buf[PATH_MAX + 1];
        snprintf(buf, PATH_MAX, "%s/%s", argv[1], content->d_name);
        struct stat file_info;
        if (stat(buf, &file_info) == 0 && S_ISREG(file_info.st_mode) &&
            file_info.st_uid == uid && isupper(content->d_name[0])) {
            size += file_info.st_size;
        }
        content = readdir(dir);
    }
    closedir(dir);
    printf("%llu\n", size); 
}