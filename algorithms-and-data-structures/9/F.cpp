#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip> 

struct point {
    double x;
    double y;
};

double sq (const std::vector<point> & fig) {
	double res = 0;
	for (int i = 0; i < fig.size(); ++i) {
		point p1 = i ? fig[i-1] : fig.back();
        point p2 = fig[i];
		res += (p1.x - p2.x) * (p1.y + p2.y);
	}
	return fabs (res) / 2;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<point> polygon(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> polygon[i].x >> polygon[i].y;
    }

    std::cout << std::fixed << std::setprecision(10) << sq(polygon) << "\n";
}

