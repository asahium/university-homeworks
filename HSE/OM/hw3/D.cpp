// # В данной задаче Вам необходимо реализовать метод Штрафов для функции:

// # f(x) = -c_1 x_1 + c_2 x_2
// # С ограничением
// # g_1 = x_1^3 - x_2 - c_3 = 0
// # x_1 >= 0, x_2 >= 0


// # Начальная точка - (2,2). Начальное значение r = 1, C = 6, каждый шаг r умножается на С, eps=1e-3.
// # Критерий остановки:

// # (r / 2) * (g(x*)) в точке x* меньше eps.

// # Формат ввода
// # Вводятся три коэффициента целевой функции и ограничения через пробел

// # Формат вывода
// # Значение целевой функции в точке минимума с округлением до 3 знака.

using namespace std;

double f(double x1, double x2, double c1, double c2) {
    return -c1 * x1 + c2 * x2;
}

double g(double x1, double x2, double c3) {
    return x1 * x1 * x1 - x2 - c3;
}

double penalty(double x1, double x2, double c1, double c2, double c3, double r) {
    return f(x1, x2, c1, c2) + r * abs(g(x1, x2, c3));
}

double penalty_method(double x1, double x2, double c1, double c2, double c3, double r, double C, double eps) {
    double x1_prev = x1, x2_prev = x2;
    double x1_next = x1, x2_next = x2;
    double r_next = r * C;
    while (r > eps) {
        x1_prev = x1_next;
        x2_prev = x2_next;
        x1_next = x1_prev - 2 * r * (3 * x1_prev * x1_prev - 1) / (6 * r + 3 * x1_prev * x1_prev * x1_prev * x1_prev);
        x2_next = x2_prev - 2 * r / (6 * r + 3 * x1_prev * x1_prev * x1_prev * x1_prev);
        r = r_next;
        r_next = r * C;
    }
    return penalty(x1_next, x2_next, c1, c2, c3, r);
}

int main() {
    double c1, c2, c3;
    std::cin >> c1 >> c2 >> c3;
    double x1 = 2, x2 = 2;
    double r = 1, C = 6, eps = 1e-3;
    cout << fixed << setprecision(3) << penalty_method(x1, x2, c1, c2, c3, r, C, eps);
    return 0;
}