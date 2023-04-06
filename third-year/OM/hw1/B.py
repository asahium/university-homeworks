def f0(x,coef):
    return (coef[0]*x-1)**2+4*(4-coef[1]*x)**4

def df0(x,coef):
    return 2*coef[0]*(coef[0]*x-1)-16*coef[1]*(4-coef[1]*x)**3

def f1(x,coef):
    return coef[0]*(x - coef[1]) + (x - coef[2])**2

def df1(x,coef):
    return coef[0] - 2*coef[2] + 2*x

def secant_search(f, df, x0, x1, coef, tol):
    x_now = x1
    ddf = (df(x_now, coef) - df(x0, coef)) / (x_now - x0)
    x_next = x_now - df(x_now, coef) / ddf

    while abs(x_now - x_next) >= tol:
        x_prev = x_now
        x_now = x_next
        ddf = (df(x_now, coef) - df(x_prev, coef)) / (x_now - x_prev)
        x_next = x_now - df(x_now, coef) / ddf
    return x_next

type_ = int(input())
f = f0 if (type_ == 0) else f1
df = df0 if (type_ == 0) else df1
coef = [i for i in map(float, input().split())]
x0, x1, tol = map(float, input().split())
r1 = secant_search(f, df, x0, x1, coef, tol)
print("{:.10f}".format(r1))