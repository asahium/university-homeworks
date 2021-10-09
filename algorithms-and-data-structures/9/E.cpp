#include <iostream>

using namespace std;
bool parall(double a1, double a2, double b1, double b2) {
    if ((a1 / a2) == (b1 / b2)) {
        cout << "Lines parallel!";
        return true;
    } else {
        return false;
    }
}
void intersect(double a1, double a2, double b1, double b2, double c1, double c2, double& x, double& y) {
    double det = a1 * b2 - a2 * b1;
    x = (b1 * c2 - b2 * c1) / det;
    y = (a2 * c1 - a1 * c2) / det;
}

int main() {
    double a1, a2, b1, b2, c1, c2;
    double x, y, x1, y1, x2, y2, x3, y3, x4, y4;
    cin >> x1 >> y1 >> x2 >> y2;
    cin >> x3 >> y3 >> x4 >> y4;
    a1 = y1 - y2;
    b1 = x2 - x1;
    c1 = x1 * y2 - x2 * y1;
    a2 = y3 - y4;
    b2 = x4 - x3;
    c2 = x3 * y4 - x4 * y3;
    
    if (parall(a1, a2, b1, b2)) {
        
    }
    
    parall(a1, a2, b1, b2);

    intersect(a1, a2, b1, b2, c1, c2, x, y);
    cout << "point of intersection " << x << " " << y << endl;
    system("pause");
    return 0;
}

