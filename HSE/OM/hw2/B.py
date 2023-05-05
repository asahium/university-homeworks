import numpy as np


def fib(n):
    if n in [0, 1]:
        return 1
    return fib(n - 1) + fib(n - 2)


def best_fib(bounds, length):
    aim = abs(bounds[1] - bounds[0]) / length
    for i in range(int(aim)):
        if fib(i) > aim:
            return i


def fib_search(f, bounds, tol, coef, max_eps=0.01):
    n = best_fib(bounds, tol)
    y = 0
    z = 0
    for k in range(n + 1):
        if k == 0:
            y = bounds[0] + fib(n-2) / fib(n) * (bounds[1] - bounds[0])
            z = bounds[0] + fib(n-1) / fib(n) * (bounds[1] - bounds[0])
        f_y = f(y, coef)
        f_z = f(z, coef)

        if f_y <= f_z:
            bounds[1] = z
            z = y
            y = bounds[0] + fib(n-k-3) / fib(n-k-1) * (bounds[1] - bounds[0])
        else:
            bounds[0] = y
            y = z
            z = bounds[0] + fib(n-k-2) / fib(n-k-1) * (bounds[1] - bounds[0])

        if k == n - 3:
            y_1 = y
            z_1 = y_1 + max_eps
            f_y = f(y_1, coef)
            f_z = f(z_1, coef)

            if f_y <= f_z:
                bounds[1] = z_1
            else:
                bounds[0] = y_1
            return (bounds[1] + bounds[0]) / 2

    return 0


def phi(t, inlet):
    f = inlet[0]
    x = inlet[1]
    d = inlet[2]
    a = inlet[3]
    b = inlet[4]
    return f(x + t * d, a, b)


def f1(x, a, b):
    return (x[0] - a) ** 2 + x[1] ** 2 + x[0] / (np.fabs(x[1]) + b)


def f2(x, a, b):
    return (x[0] - a) ** 2 + x[0] * x[1] + (x[1] - b) ** 2


def df1_1(x, a, b):
    return -2 * a + 1 / (np.fabs(x[1]) + b) + 2 * x[0]


def df1_2(x, a, b):
    return 2 * x[1] - (x[0] * x[1]) / (np.fabs(x[1]) * (np.fabs(x[1]) + b) ** 2)


def df2_1(x, a, b):
    return -2 * a + 2 * x[0] + x[1]


def df2_2(x, a, b):
    return -2 * b + x[0] + 2 * x[1]


def fletcher_reeves(f, df, a, b, x0, M, t0, eps1, eps2):
    xs = list()
    xs.append(x0)
    # beta = list()
    d = 0
    for k in range(M):
        grad = np.array([df[0](xs[k], a, b), df[1](xs[k], a, b)])
        if np.linalg.norm(grad) < eps1:
            return xs[k]
        if k == 0:
            d = grad * -1
        else:
            beta = (np.linalg.norm(np.array([df[0](xs[k], a, b), df[1](xs[k], a, b)])) ** 2) / (
                        np.linalg.norm(np.array([df[0](xs[k - 1], a, b), df[1](xs[k - 1], a, b)])) ** 2)
            d = -1 * grad + beta * d
        t_k = fib_search(phi, [0, 1], 0.0001, [f, xs[k], d, a, b], max_eps=0.01)
        xs.append(0)
        xs[k + 1] = xs[k] + t_k * d
        if k >= 3:
            if np.linalg.norm(xs[k + 1] - xs[k]) < eps2 and np.abs(
                    f(xs[k + 1], a, b) - f(xs[k], a, b)) < eps2 and np.linalg.norm(xs[k] - xs[k - 1]) < eps2 and np.abs(
                    f(xs[k], a, b) - f(xs[k - 1], a, b)) < eps2:
                return xs[k]
    return None


typ = int(input())
a, b = map(float, input().split(" "))
if typ == 0:
    f = f1
    df = [df1_1, df1_2]
else:
    f = f2
    df = [df2_1, df2_2]
eps1, eps2 = map(float, input().split(" "))
x1, x2 = map(float, input().split(" "))
x = [x1, x2]
x_opt = fletcher_reeves(f, df, a, b, x, 10000, 0.5, eps1, eps2)
print(f(x_opt, a, b))
