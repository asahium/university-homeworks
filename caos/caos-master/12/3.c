#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


struct FileContent eoe(struct FileContent result) {
    free(result.data);

    result.data = NULL;
    result.size = -1;

    return result;
}

struct FileContent read_file(int fd) {
    struct FileContent result;
    result.size = 0;
    result.data = NULL;

    char buf[4096];

    int actual;

    while ((actual = read(fd, buf, 4096))) {
        if (actual < 0)
            return eoe(result);

        char * tmp = realloc(result.data, result.size + actual);

        if (!tmp)
            return eoe(result);

        result.data = tmp;

        memcpy(result.data + result.size, buf, actual);

        result.size += actual;
    }

    char * tmp = realloc(result.data, result.size + 1);

    if (!tmp)
        return eoe(result);

    result.data = tmp;
    result.data[result.size] = '\0';

    return result;
}