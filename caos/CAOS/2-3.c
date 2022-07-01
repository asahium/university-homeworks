int bitcount(STYPE value) {
    UTYPE copy = value;
    int ans = 0;
    while (copy) {
        ans += copy & 1;
        copy >>= 1;
    }
    return ans;
}