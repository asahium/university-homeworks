// Comment by Judge: Для всей функции достаточно двух сравнений. Оптимизируйте код.



int mystrcmp(const char *str1, const char *str2) {
    const unsigned char* string1 = (const unsigned char*)str1;
    const unsigned char* string2 = (const unsigned char*)str2;
    while (*string1 && *string2) {
        if (*string1 < *string2) {
            return -1;
        } else if (*string1 > *string2) {
            return 1;
        } else {
        ++string1;
        ++string2;
        }
    }
    if (*string1) {
        return 1;
    }
    if (*string2) {
        return -1;
    }
    return 0;
}
