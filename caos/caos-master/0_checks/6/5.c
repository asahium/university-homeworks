#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <dirent.h>
#include <string.h>

int main(int argc, char ** argv) {
    unsigned long long criterion = strtoull(argv[2], NULL, 0);

    char * max_file_name = NULL;
    off_t max_file_size = 0;

    int print = 0;

    DIR* dir = opendir(argv[1]);

    if (!dir)
        return 1;

    struct dirent* dir_item;
    struct stat file_stat;

    char item_path[PATH_MAX + 1];

    while ((dir_item = readdir(dir))) {
        char * item_name = dir_item->d_name;

        if (!strcmp(item_name, "."))
            continue;

        if (!strcmp(item_name, ".."))
            continue;

        strcpy(item_path, argv[1]);
        strcat(item_path, "/");
        strcat(item_path, item_name);

        int id = lstat(item_path, &file_stat);

        if (id < 0)
            continue;

        if (!S_ISREG(file_stat.st_mode))
            continue;

        if (S_ISLNK(file_stat.st_mode))
            continue;

        if (file_stat.st_size > max_file_size ||(
            file_stat.st_size == max_file_size &&
            (!max_file_name || strcmp(item_name, max_file_name) <= 0))) {
            max_file_name = item_name;
            max_file_size = file_stat.st_size;
        }

        if (print)
            continue;

        if (criterion >= file_stat.st_size) {
            criterion -= file_stat.st_size;
        } else {
            print = 1;
        }
    }

    if (print)
        printf("%s", max_file_name);

    closedir(dir);
}