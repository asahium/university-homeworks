int bitcount(STYPE value) {
    int res = 0;

    UTYPE copy = value;

    while (copy) {
        res += copy & 1;
        copy >>= 1;
    }

    return res;
}
