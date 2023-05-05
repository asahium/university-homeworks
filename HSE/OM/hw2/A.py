import numpy as np


def f1(x, a, b):
    return a * np.sin(x[0]) + b * np.cos(x[1])


def f2(x, a, b):
    return (x[0] - a) ** 2 + x[0] * x[1] + (x[1] - b) ** 2


def df1_1(x, a, b):
    return a * np.cos(x[0])


def df1_2(x, a, b):
    return -b * np.sin(x[1])


def df2_1(x, a, b):
    return -2 * a + 2 * x[0] + x[1]


def df2_2(x, a, b):
    return -2 * b + x[0] + 2 * x[1]


def coordinate_descent(f, df, a, b, x_0, max_iter, t_0, eps1, eps2):
    t_k = t_0
    x_diff = list()
    f_diff = list()
    xs = list()
    xs.append([])
    xs[0].append(x_0)
    for j in range(max_iter):
        k = 0
        while True:
            if k == 2:
                xs.append([])
                xs[j + 1].append(xs[j][k])
                break
            grad = np.array([df[0](xs[j][k], a, b), df[1](xs[j][k], a, b)])
            if np.linalg.norm(grad) < eps1:
                return xs[j][k]
            l = np.zeros(2)
            l[k] = 1
            xs[j].append([])
            xs[j][k+1] = xs[j][k] - t_k * df[k](xs[j][k], a, b) * l
            if f(xs[j][k+1], a, b) - f(xs[j][k], a, b) >= 0:
                t_k = t_k / 2
            else:
                if j > 0:
                    if np.linalg.norm(xs[j][k+1] - xs[j][k]) < eps2 and np.abs(f(xs[j][k+1], a, b) - f(xs[j][k], a, b)) < eps2 and np.linalg.norm(xs[j - 1][k+1] - xs[j - 1][k]) < eps2 and np.abs(f(xs[j-1][k + 1], a, b) - f(xs[j-1][k], a, b)) < eps2:
                        return xs[j][k+1]
                    else:
                        k = k + 1
                else:
                    k = k + 1

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
x_opt = coordinate_descent(f, df, a, b, x, 10000, 0.5, eps1, eps2)
print(f(x_opt, a, b))
