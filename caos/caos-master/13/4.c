#include <stddef.h>
const char *perms_to_str(char *r, size_t s, int p) {
    if (!(s--)) { return r; }
    char * a = "rwxrwxrwx";
    for (int i = 0; i < 9; ++i) { if (!(p & (1 << i))) { a[i] = '-'; } }
    if (p & 2057) { a[2] = 's'; }
    if (p & 1025) { a[5] = 's'; }
    if (p & 515) { a[8] = 't'; }
    for (int i = 0; (i < 9) && (i < s); ++i) { *(r++) = a[i]; }
    return (*r = '\0') - 1 + r - s;
}
