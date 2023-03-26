def f0(x,coef):
    return coef[0]*x**2 + coef[1]*x + coef[2]

def f1(x,coef):
    return coef[0]*x**4 + coef[1]*x**3 + coef[2]*x**2 + coef[3]*x + coef[4]

def fib(n):
    if n in [0,1]:
        return 1
    return fib(n - 1) + fib(n - 2)

def fun(bounds, l):
    for i in range(int(abs(bounds[1] - bounds[0]) / l)):
        if fib(i) > abs(bounds[1] - bounds[0]) / l:
            return i

def fib_search(f, bounds, tol, coef, max_eps = 0.01):
    n = fun(bounds, tol)
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


type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
bounds = [0, 0]
bounds[0], bounds[1], tol = map(float, input().split())
r1 = fib_search(f, bounds, tol, coef)
print("{:.10f}".format(r1))