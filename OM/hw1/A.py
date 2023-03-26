def f0(x,coef):
    return coef[0]*x**2 + coef[1]*x + coef[2]

def f1(x,coef):
    return coef[0]*x**4 + coef[1]*x**3 + coef[2]*x**2 + coef[3]*x + coef[4]

def fib(n):
    if n in [0,1]:
        return 1
    return fib(n - 1) + fib(n - 2)

def fib_search(f, bounds, tol, coef, max_eps = 0.01):
    #Your Code
    return 0


type = int(input())
f = f0 if (type == 0) else f1
coef = [i for i in map(float,input().split())]
bounds = [0, 0]
bounds[0], bounds[1], tol = map(float, input().split())
r1 = fib_search(f, bounds, tol, coef)
print("{:.10f}".format(r1))