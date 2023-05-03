#include <algorithm>
#include <iostream>
#include <cmath>
#include <complex>
#include <vector>

#define pi 3.1415926535897932384

std::vector<std::complex<double>> fastfurie(std::vector<std::complex<double>> &a, std::complex<double> w) {
    auto z = a.size();

    if (z == 1) {
        return std::vector({a[0]});
    }

    std::vector<std::complex<double>> a0(z / 2), a1(z / 2);
    for (int i = 0; i < z / 2; ++i) {
        a0[i] = a[2 * i];
        a1[i] = a[2 * i + 1];
    }
    auto u0 = fastfurie(a0, w * w);
    auto u1 = fastfurie(a1, w * w);

    std::vector<std::complex<double>> u(z);

    auto p = std::complex<double>(1);
    for (int i = 0; i < z; ++i) {
        u[i] = u0[i % (z / 2)] + p * u1[i % (z / 2)];
        p *= w;
    }

    return u;
}

std::vector<std::complex<double>> reversefastfurie(std::vector<std::complex<double>> &a, std::complex<double> w) {
    auto res = fastfurie(a, w);
    auto num = res.size();

    for (int j = 0; j < num; ++j) {
        res[j] /= num;
    }
    reverse(res.begin() + 1, res.end());

    return res;
}

void intovec(std::vector<std::complex<double>> & v, std::string & s) {
    int i = s[0] == '-';

    for (int j = (int) s.size() - 1; j >= i; --j) {
        v[s.size() - 1 - j] = s[j] - '0';
    }

    for (int j = (int) v.size() - i; j < v.size(); ++j) {
        v[j] = 0;
    }
}

void start(size_t &n) {
    size_t incn = 1;

    while (incn < n) {
        incn <<= 1;
    }

    n = 2 * incn;
}

std::vector<int> tonum(std::vector<std::complex<double>> const &a) {
    auto n = a.size();

    std::vector<int> ans(n);

    for (int i = 0; i < n; ++i) {
        ans[i] = (int) (a[i].real() + 0.5);
    }

    int r = 0;

    for (int i = 0; i < n; ++i) {
        ans[i] += r;
        r = ans[i] / 10;
        ans[i] %= 10;
    }

    while (ans.back() == 0) {
        ans.pop_back();
    }

    return ans;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s1, s2;
    std::cin >> s1 >> s2;

    if (s1 == "0" || s2 == "0") {
        std::cout << 0;
        return 0;
    }
    int i = s1[0] == '-';
    int j = s2[0] == '-';

    int sign = (i == 0 ? 1 : -1) * (j == 0 ? 1 : -1);

    size_t n;
    n = std::max(s1.size() - i, s2.size() - j);
    start(n);

    std::vector<std::complex<double>> first(n);

    std::vector<std::complex<double>> second(n);

    intovec(first, s1);

    intovec(second, s2);

    double ang = 2 * pi / n;

    std::complex<double> w(cos(ang), sin(ang));

    auto u = fastfurie(first, w);

    auto v = fastfurie(second, w);

    std::vector<std::complex<double>> answer(n);
    for (int i = 0; i < n; ++i) {
        answer[i] = u[i] * v[i];
    }

    auto ans = tonum(reversefastfurie(answer, w));

    if (sign == -1) {
        std::cout << '-';
    }
    for (int i = ans.size() - 1; i >= 0; --i) {
        std::cout << ans[i];
    }

    return 0;
}

