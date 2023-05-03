#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

struct point {
    double x;
    double y;
};

point tr(point a, point b) {
    point ans;
    ans.x = a.x - b.x;
    ans.y = a.y - b.y;
    return ans;
}

int m(point a, point b) {
    return a.x * b.y - a.y * b.x;
}

int main() {
    int n;
    point dot;
    std::cin >> n >> dot.x >> dot.y;
    std::vector<point> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i].x >> a[i].y;
    }
    int c = 0;
    point last = a[0];
    a.push_back(last);
    for (int i = 1; i < n+1; ++i) {
        if ((dot.x == a[i].x) && (dot.y == a[i].y)) {
            std::cout << "YES";
            return 0;
        } else {
            if ((dot.y >= std::min(last.y, a[i].y)) && (dot.y < std::max(last.y, a[i].y))) {
                std::pair<point, point> t;
                if (last.y < a[i].y) {
                    t.first = last;
                    t.second = a[i];
                } else {
                    t.second = last;
                    t.first = a[i];
                }
                if (m(tr(t.second, t.first), tr(dot, t.first)) == 0) {
                    std::cout << "YES";
                    return 0;
                }

                if (m(tr(t.second, t.first), tr(dot, t.first)) >= 0) {
                    c += 1;
                }
            }
        }
        last = a[i];
    }

    if (c % 2 == 0) {
        std::cout << "NO";
    } else {
        std::cout << "YES";
    }

    return 0;
}

