int mystrcmp(const char *a, const char *b) {
    const unsigned char * str1 = (const unsigned char *)a;
    const unsigned char * str2 = (const unsigned char *)b;
    
    while (*str1 && *str2) {
        if (*str1 < *str2)
            return -1;
        if (*str1 > *str2)
            return 1;
        ++str1;
        ++str2;
    }

    if (*str1)
        return 1;

    if (*str2)
        return -1;

    return 0;
}
