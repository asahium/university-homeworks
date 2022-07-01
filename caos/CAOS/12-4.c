#include <stddef.h>

const char *perms_to_str(char *buf, size_t size, int perms) {
    if (!size) { 
        return buf; 
    }
    char str[] = "rwxrwxrwx";
    for (int i = 0; i < 9; ++i) {
        if (!(perms & (1 << i))) {
            str[8 - i] = '-';
        }
    }
    if (perms & 04000) {
        str[2] = 's';
    }
    if (perms & 02000) {
        str[5] = 's';
    }
    if (perms & 01000) {
        str[8] = 't';
    }
    for (int i = 0; (i < 9) && (i < size - 1); ++i) {
        *(buf++) = str[i];
    }
    *buf = '\0';
    return buf;
}