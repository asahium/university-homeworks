#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

using namespace std;
typedef long long ll;

class point {
public:
    ll x, y;
    point() :x(), y() {
    }
    point(ll x, ll y) :x(x), y(y) {

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
    ll n, m, r;
    cin >> n >> m >> r;

    vector<point> a(n);
    vector<set<point> > kek(1);
    for(int i = 0; i < n; ++i) {
        cin >> a[i].x >> a[i].y;
        kek[0].insert(a[i]);
    }

    for(int i = 0; i < m; ++i) {
        ll A, B, C;
        cin >> A >> B >> C;

        int Q = kek.size();
        for(int q = 0; q < Q; ++q) {
            set<point> &lol = kek[q];
            set<point> l, r;
            for(auto d : lol) {
                if(A * d.x + B * d.y + C > 0)
                    l.insert(d);
                else
                    r.insert(d);
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
