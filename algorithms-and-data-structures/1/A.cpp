#include <algorithm>
#include <iostream>

struct Point {
    int x;
    int y;
};

struct SegmentIntersection {
    inline bool intersect(Point x1, Point x2, Point x3, Point x4) {
        int d1 = direction(x3, x4, x1);
        int d2 = direction(x3, x4, x2);
        int d3 = direction(x1, x2, x3);
        int d4 = direction(x1, x2, x4);

        if ((((d1 > 0) && (d2 < 0)) || ((d1 < 0) && (d2 > 0))) && (((d3 > 0) && (d4 < 0)) || ((d3 < 0) && (d4 > 0))))
            return true;

        else if (d1 == 0 && on_segment(x3, x4, x1))
            return true;

        else if (d2 == 0 && on_segment(x3, x4, x2))
            return true;

        else if (d3 == 0 && on_segment(x1, x2, x3))
            return true;

        else if (d4 == 0 && on_segment(x1, x2, x4))
            return true;

        else
            return false;
    }

    inline int direction(Point x1, Point x2, Point x3) {
        return ((x3.x - x1.x) * (x2.y - x1.y)) -
               ((x2.x - x1.x) * (x3.y - x1.y));
    }

    inline bool on_segment(Point x1, Point x2,
                           Point x3) {
        if (std::min(x1.x, x2.x) <= x3.x &&
            x3.x <= std::max(x1.x, x2.x) &&
            std::min(x1.y, x2.y) <= x3.y &&
            x3.y <= std::max(x1.y, x2.y))
            return true;

        else
            return false;
    }
};

int main() {
    SegmentIntersection segment;
    Point x1, x2, x3, x4;
    std::cin >> x1.x >> x1.y;
    std::cin >> x2.x >> x2.y;
    std::cin >> x3.x >> x3.y;
    std::cin >> x4.x >> x4.y;
    if (segment.intersect(x1, x2, x3, x4)) {
        std::cout << "YES";
    } else {
        std::cout << "NO";
    }
}
