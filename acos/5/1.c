void normalize_path(char *buf) {
    char *old = buf;
    char *new = buf;
    int c = 0;
    while (*old != '\0') {
        if (*old == '/') {
            if (c) {
                ++old;
            } else {
                *new = *old;
                ++old;
                ++new;
                c = 1;
            }
        } else {
            *new = *old;
            ++old;
            ++new;
            c = 0;
        }
    }
    *new = '\0';
}
