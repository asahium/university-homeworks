#include <stddef.h>

struct BSearchResult {
    size_t low;
    size_t high;
    int result;
};

struct BSearchResult bsearch2(
    const void *key,
    const void *base,
    size_t nmemb,
    size_t size,
    int (*compar)(const void *p1, const void *p2, void *user),
    void *user) {
    struct BSearchResult output = {0, 0, 0};
    size_t l = 0;
    size_t r = nmemb;
    size_t m;
    int ans;
    while (l < r) {
        m = l + (r - l) / 2;
        ans = (*compar)(key, base + size * m, user);
        if (ans) {
            if (ans < 0) {
                r = m;
            } else {
                l = m + 1;
            }
        } else {
            output.result = 1;
            r = m;
        }
    }
    output.low = l;
    l = 0;
    r = nmemb;
    while (l < r) {
        m = l + (r - l) / 2;
        ans = (*compar)(key, base + size * m, user);
        if (ans >= 0) {
            l = m + 1;
        } else {
            r = m;
        }
    }
    output.high = l;
    return output;
}