import numpy as np


def f0(x, coef):
    return (4*(x[0] - coef[0])**2 + (x[1] - coef[1])**2)
def f1(x, coef):
    return (x[0]-coef[0])**2 + x[0]*x[1] + coef[1]*(x[1]-3)**2


def func(f, x_in, coef):
    sup = np.array([f(x_in[0], coef), f(x_in[1], coef), f(x_in[2], coef)])
    ind = np.argsort(sup)
    minn = x_in[ind[0]]
    midd = x_in[ind[1]]
    maxx = x_in[ind[2]]
    return minn, midd, maxx


def Nealder_Mead(f, x0, tol, coef):
    al = 1
    beta = 0.5
    gam = 3
    k = 0
    x = x0
    while True:
        xl, xs, xh = func(f, x, coef)
        centr = (xl + xs) / 2
        sigma = np.sqrt(1 / 3 * ((f(xl, coef) - f(centr, coef)) ** 2 + (f(xs, coef) - f(centr, coef)) ** 2 + (
                    f(xh, coef) - f(centr, coef)) ** 2))
        if sigma < tol:
            return f(xl, coef)
        x_sup3 = centr + al * (centr - xh)
        if f(x_sup3, coef) <= f(xl, coef):
            x_sup4 = centr + gam * (x_sup3 - centr)
            if f(x_sup4, coef) < f(xl, coef):
                x = [xl, xs, x_sup4]
                continue
            else:
                x = [xl, xs, x_sup3]
                continue
        if f(xs, coef) < f(x_sup3, coef) <= f(xh, coef):
            x_sup5 = centr + beta * (xh - centr)
            x = [xl, xs, x_sup5]
            continue
        if f(xl, coef) < f(x_sup3, coef) <= f(xs, coef):
            x = [xl, xs, x_sup3]
            continue
        if f(x_sup3, coef) > f(xh, coef):
            for i in range(3):
                x[i] = xl + 0.5*(x[i] - xl)
        k += 1
    return 0, 0


type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float, input().split())]
x0 = []
for k in range(3):
    x0.append(np.array([i for i in map(float, input().split())]))
tol = float(input())
r1 = Nealder_Mead(f, x0, tol, coef)
print("{:.10f}".format(r1))