### Условие

Выведите все исходные точки в порядке возрастания их расстояний от начала координат. Создайте структуру Point и сохраните исходные данные в массиве структур Point.
Формат ввода

Программа получает на вход набор точек на плоскости. Сначала задано количество точек n, затем идет последовательность из n строк, каждая из которых содержит два числа: координаты точки. Величина n не превосходит 100, все исходные координаты – целые числа, не превосходящие 103.
Формат вывода

Необходимо вывести все исходные точки в порядке возрастания их расстояний от начала координат. 
### Решение

```cpp
#include <algorithm>
#include <iostream>
#include <math.h>
#include <vector>

struct Point {
    int x, y;
    Point() {}
    Point(int x, int y) : x(x), y(y) {}
};

bool compare(Point a, Point b) {
    return sqrt(a.x * a.x + a.y * a.y) < sqrt(b.x * b.x + b.y * b.y);
}

int main() {
    int n;
    std::cin >> n;
    std::vector <Point> a(n);
    for (int i = 0; i < n; ++i) {
        int x, y;
        std::cin >> x >> y;
        a[i] = {x, y};
    }
    std::sort(a.begin(), a.end(), compare);
    for (auto d : a) {
        std::cout << d.x << " " << d.y << "\n";
    }

    return 0;
}

```

