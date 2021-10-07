#include <iostream>
using namespace std;
 
void main() {
    double x1, y1, x2, y2, k, b;
    cin >> x1 >> y1 >> x2 >> y2;
 
    k = (y2 - y1)/(x2 - x1);
    b = (x2*y1 - x1*y2)/(x2 - x1);
    cout<< k << b <<"\n";
 
    return 0;
}
