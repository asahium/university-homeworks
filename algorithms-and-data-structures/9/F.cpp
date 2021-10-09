#include <iostream>
#include <cmath>

struct point {
    int x;
    int y;
};

double getArea(point *p, unsigned size) {
    double result = 0.0;
    for (unsigned i = 0, j = 1; i < size; j = (++i + 1) % size) {
        result += (p[j].x - p[i].x)  *  (p[j].y + p[i].y);
    }
    return fabs(0.5*result);
}

int main() {
    int n;
    std::cin >> n;
    point polygon[n];
    for (int i = 0; i < n; ++i){
        std::cin >> polygon[i].x >> polygon[i].y;
    }

    std::cout << getArea(polygon, n) << "\n";
}

