void normalize_path(char *t1) {
    char *fast = t1;
    char *slow = t1;

    int s = 0;

    while (*fast != '\0') {
        if (*fast == '/') {
            if (s) {
                ++fast;
            } else {
                *slow = *fast;
                ++slow;
                ++fast;
                s = 1;
            }
        } else {
            *slow = *fast;
            ++slow;
            ++fast;
            s = 0;
        }
    }

    *slow = '\0';
}
