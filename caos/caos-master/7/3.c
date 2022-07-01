#include <stddef.h>

struct BSearchResult
{
    size_t low;
    size_t high;
    int result;
};

struct BSearchResult bsearch2( const void *key, const void *base,
        size_t nmemb, size_t size,
        int (*compar)(const void *p1, const void *p2, void *user),
        void *user) {
    struct BSearchResult output = {0, 0, 0};

    size_t l = 0;
    size_t r = nmemb;
    size_t middle;

    int ans;

    while (l < r) {
        middle = l + (r - l) / 2;

        ans = (*compar)(key, base + size * middle, user);

        if (ans) {
            ans < 0 ? (r = middle) : (l = middle + 1);
        } else {
            output.result = 1;
            r = middle;
        }
    }

    output.low = l;

    l = 0;
    r = nmemb;

    while (l < r) {
        middle = l + (r - l) / 2;

        (*compar)(key, base + size * middle, user) >= 0 ?
        (l = middle + 1) : (r = middle);
    }

    output.high = l;

    return output;
}