#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

struct FileContent refresh(struct FileContent res) {
    free(res.data);
    res.data = NULL;
    res.size = -1;
    return res;
}

struct FileContent read_file(int fd) {
    struct FileContent res;
    res.data = NULL;
    res.size = 0;
    char buffer[4096];
    int cur;

    while ((cur = read(fd, buffer, 4096))) {
        if (cur < 0) {
            return refresh(res);
        }
        char* tmp = realloc(res.data, res.size + cur);
        if (!tmp) {
            return refresh(res);
        }
        res.data = tmp;
        memcpy(res.data + res.size, buffer, cur);
        res.size += cur;
    }
    char* tmp = realloc(res.data, res.size + 1);
    if (!tmp) {
        return refresh(res);
    }
    res.data = tmp;
    res.data[res.size] = '\0';
    return res;
}