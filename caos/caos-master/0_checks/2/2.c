int mystrpunktcmp(const char *one, const char *two) {
    const unsigned char * a = (unsigned char *) one;
    const unsigned char * b = (unsigned char *) two;
    while (*a && *b) {
        while (*a == '.' || *a == ',' || *a == ':' || *a == ';' || *a == '!' || *a == '?') {
            ++a;
        }
        while (*b == '.' || *b == ',' || *b == ':' || *b == ';' || *b == '!' || *b == '?') {
            ++b;
        }

        if (!*a)
            break;

        if (!*b)
            break;

        if (*a > *b) {
            return 1;
        } else if (*a < *b) {
            return -1;
        } else {
            ++a;
            ++b;
        }
    }
    while (*a == '.' || *a == ',' || *a == ':' || *a == ';' || *a == '!' || *a == '?')
        ++a;
    while (*b == '.' || *b == ',' || *b == ':' || *b == ';' || *b == '!' || *b == '?')
        ++b;

    if (*a) {
        return 1;
    }

    if (*b) {
        return -1;
    }

    return 0;
}
