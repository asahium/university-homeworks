import numpy as np

def f0(x,coef):
    return (4*(x[0] - coef[0])**2 + (x[1] - coef[1])**2)
def f1(x,coef):
    return (x[0]-coef[0])**2 + x[0]*x[1] + coef[1]*(x[1]-3)**2

def func(f, x, coef):
    sup = np.array([f(x[0], coef), f(x[1], coef), f(x[2], coef)])
    ind = np.argsort(sup)
    xl = x[ind[0]]
    xs = x[ind[1]]
    xh = x[ind[2]]
    return xl, xs, xh

def Nealder_Mead(f, x0, tol, coef):
    al = 1
    beta = 0.5
    gam = 2
    k, x = 0, np.array(x0)

    while True:
        xl, xs, xh = func(f, x, coef)
        c = (xl + xs) / 2
        s = np.sqrt(1 / 3 * ((f(xl, coef) - f(c, coef)) ** 2 + (f(xs, coef) - f(c, coef)) ** 2 + (f(xh, coef) - f(c, coef)) ** 2))

        if s < tol:
            return f(xl, coef)

        x3 = c + al * (c - xh)

        if f(x3, coef) <= f(xl, coef):
            x4 = c + gam * (x3 - c)

            if f(x4, coef) < f(xl, coef):
                x = [xl, xs, x4]
                continue
            else:
                x = [xl, xs, x3]
                continue

        if f(xs, coef) < f(x3, coef) <= f(xh, coef):
            x5 = c + beta * (xh - c)
            x = [xl, xs, x5]
            continue

        if f(xl, coef) < f(x3, coef) <= f(xs, coef):
            x = [xl, xs, x3]
            continue

        if f(x3, coef) > f(xh, coef):
            for i in range(3):
                x[i] = xl + 0.5*(x[i] - xl)
        k += 1

    return 0, 0

type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
x0 = []
for k in range(3):
    x0.append(np.array([i for i in map(float,input().split())]))
tol = float(input())
r1 = Nealder_Mead(f, x0, tol, coef)
print("{:.10f}".format(r1))