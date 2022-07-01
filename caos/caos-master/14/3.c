#include <ctype.h>
#include <dirent.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <unistd.h>

int compare(const void * a, const void * b) {
    return strcasecmp(*(char* const*) a, *(char* const*) b);
}

void process(char * path, char * name, int s) {
    if (strlen(path) >= PATH_MAX)
        return;

    DIR *dir = opendir(path);

    if (!dir)
        return;

    if (!s)
        printf("cd %s\n", name);

    char path_str[PATH_MAX];

    strcpy(path_str, path);
    strcat(path_str, "/");
    strcat(path_str, name);

    struct dirent * entry;

    char ** subdirs = malloc(100 * sizeof(char*));

    uint64_t count = 0;
    uint64_t capacity = 100;

    while ((entry = readdir(dir))) {
        if (!strcmp(entry->d_name, ".") || !strcmp(entry->d_name, ".."))
            continue;

        if (strlen(entry->d_name) >= PATH_MAX)
            continue;

        if (entry->d_type != DT_DIR)
            continue;

        if (count == capacity) {
            capacity *= 2;
            subdirs = realloc(subdirs, capacity * sizeof(char*));
        }

        subdirs[count] = malloc(strlen(entry->d_name) + 1);
        strcpy(subdirs[count], entry->d_name);

        ++count;
    }

    closedir(dir);

    if (count > 1)
        qsort(subdirs, count, sizeof(char *), compare);

    for (int i = 0; i < count; ++i) {
        process(path_str, subdirs[i], 0);
        free(subdirs[i]);
    }

    free(subdirs);

    if (!s)
        printf("cd ..\n");
}

int main(int argc, char **argv) {
    process(argv[1], "", 1);
}