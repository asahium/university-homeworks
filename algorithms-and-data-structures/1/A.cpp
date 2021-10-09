#include <iostream>
#include <cmath>
#include <vector>

struct point {
    int x;
    int y;
};

double sq (const std::vector<point> & fig) {
	double res = 0;
	for (unsigned i=0; i<fig.size(); i++) {
		point p1 = i ? fig[i-1] : fig.back();
        point p2 = fig[i];
		res += (p1.x - p2.x) * (p1.y + p2.y);
	}
	return fabs (res) / 2;
}

int main() {
    int a, b;
    std::cin >> a >> b;
    double c = a / b;
    std::cout << c;
}
