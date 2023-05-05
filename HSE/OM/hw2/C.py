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


def f(x, a, b):
    return (x[0] - x[1] ** 2) ** 2 + (a - x[0]) ** 2 + b


def df_1(x, a, b):
    return -2 * (a - 2 * x[0] + x[1] ** 2)


def df_2(x, a, b):
    return -4 * x[1] * (x[0] - x[1] ** 2)


def df_1_1(x, a, b):
    return 4


def df_1_2(x, a, b):
    return -4 * x[1]


def df_2_2(x, a, b):
    return -4 * (x[0] - 3 * x[1] ** 2)


def df_2_1(x, a, b):
    return -4 * x[1]


def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)


def ft(t, dk, x, f, a, b):
    x += t * dk
    return f(x, a, b)


def newton_method(f, df, H, a, b, x0, M, t0, eps1, eps2):
    xs = list()
    xs.append(x0)
    for k in range(M):
        grad = np.array([df[0](xs[k], a, b), df[1](xs[k], a, b)])
        if np.linalg.norm(grad) < eps1:
            return xs[k]
        h_counted = np.array(
            [[H[0][0](xs[k], a, b), H[0][1](xs[k], a, b)], [H[1][0](xs[k], a, b), H[1][1](xs[k], a, b)]])
        h_inv = np.linalg.inv(h_counted)
        if is_pos_def(h_inv):
            d = np.dot((-1 * h_inv), grad)
            t_k = 1
        else:
            d = -1 * grad
            t_k = fib_search(phi, [0, 1], 0.0001, [f, xs[k], d, a, b], max_eps=0.01)
        xs.append(0)
        xs[k + 1] = xs[k] + t_k * d
        if k >= 3:
            if np.linalg.norm(xs[k + 1] - xs[k]) < eps2 and np.abs(
                    f(xs[k + 1], a, b) - f(xs[k], a, b)) < eps2 and np.linalg.norm(xs[k] - xs[k - 1]) < eps2 and np.abs(
                    f(xs[k], a, b) - f(xs[k - 1], a, b)) < eps2:
                return xs[k]
    return xs[-1]


a, b = map(float, input().split(" "))
f = f
df = [df_1, df_2]
H = [[df_1_1, df_1_2], [df_2_1, df_2_2]]
eps1, eps2 = map(float, input().split(" "))
x1, x2 = map(float, input().split(" "))
x = [x1, x2]
x_opt = newton_method(f, df, H, a, b, x, 10000, 0.5, eps1, eps2)
print(f(x_opt, a, b))
