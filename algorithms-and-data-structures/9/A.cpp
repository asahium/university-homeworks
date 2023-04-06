#include <iostream>
using namespace std;

int main() {
    int x1, y1, x2, y2, A, B, C;
    cin >> x1 >> y1 >> x2 >> y2;

    A = y2 - y1;
    B = x1 - x2;
    C = x2*y1 - x1*y2;
    cout<< A << ' ' << B << ' ' << C <<"\n";

    return 0;
}

