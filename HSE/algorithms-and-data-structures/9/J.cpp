#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

using namespace std;

class point {
public:
    int x, y;
    point() :x(), y() {
    }
    point(int x, int y) :x(x), y(y) {

    }
    point operator+(point b) {
        return {x + b.x, y + b.y};
    }
    point operator-(point b) {
        return {x - b.x, y - b.y};
    }
    bool operator<(const point& b) const {
        return x < b.x || (x == b.x && y < b.y);
    }
    bool operator==(const point& b) const {
        return x == b.x && y == b.y;
    }
    bool operator!=(const point& b) const {
        return !(x == y);
    }
};

int main() {
    int n, m, r;
    cin >> n >> m >> r;

    vector<point> a(n);
    vector<vector<point> > kek(1);
    for(int i = 0; i < n; ++i) {
        cin >> a[i].x >> a[i].y;
        kek[0].push_back(a[i]);
    }

    for(int i = 0; i < m; ++i) {
        int A, B, C;
        cin >> A >> B >> C;

        int Q = kek.size();
        for(int q = 0; q < Q; ++q) {
            vector<point> &lol = kek[q];
            vector<point> l, r;
            for(auto d : lol) {
                if(A * d.x + B * d.y + C > 0)
                    l.push_back(d);
                else
                    r.push_back(d);
            }
            if(l.empty() || r.empty())
                continue;
            kek[q] = l;
            kek.push_back(r);
        }
    }
    cout << (kek.size() == n ? "NO" : "YES");
    return 0;
}
