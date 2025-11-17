#include <iostream>
#include <algorithm>

int main() {
    int x0, y0, x1, y1, x2, y2;
    std::cin >> x0 >> y0 >> x1 >> y1 >> x2 >> y2;

    if ((x0 - x1) * (y2 - y1) == (x2 - x1) * (y0 - y1)) {
        if (std::min(y1, y2) <= y0 && (std::max(y1, y2) >= y0) && std::min(x1, x2) <= x0 && std::max(x1, x2) >= x0){
            std::cout << "YES";
            return 0;
        }
    }
    std::cout << "NO";
}

