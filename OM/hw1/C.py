import numpy as np

def f0(x,coef):
    return coef[0]*x[0]**4 + coef[1]*x[1]**3 + coef[2]*x[1]**2 + coef[3]*x[0] + coef[4]
def f1(x,coef):
    return x[0]**2 + coef[0]*x[0]*x[1] + coef[1]*(x[1]-3)**2

def Hooke_Jeeves(f, x0, tol, coef):
    delta = np.array([1.0, 1.0])
    al = 2
    lam = 1
    xs = list()
    xs.append(x0)
    d = np.eye(2)
    y = [0, 0, 0]
    y[0] = x0
    k, i = 0, 0

    while np.any(delta >= tol):
        if f(y[i] + delta * d[:, i], coef) < f(y[i], coef):
            y[i + 1] = y[i] + delta * d[:, i]
            
        elif f(y[i] - delta * d[:, i], coef) < f(y[i], coef):
            y[i + 1] = y[i] - delta * d[:, i]

        else:
            y[i + 1] = y[i]

        if i < 1:
            i += 1

        else:
            if f(y[2], coef) < f(xs[k], coef):
                xs.append(y[2])
                y = [xs[k+1] + lam * (xs[k+1] - xs[k]), 0, 0]
                k, i = k + 1, 0
                continue

            else:
                if np.any(delta <= tol):
                    return xs[k]

                else:
                    delta[delta > tol] /= al
                    y = [xs[k], 0, 0]
                    xs.append(xs[k])
                    k, i = k + 1, 0
                    continue
                
    return xs[-1]


type_ = int(input())
f = f0 if (type_ == 0) else f1
coef = [i for i in map(float,input().split())]
x0 = np.array([i for i in map(float,input().split())])
tol = float(input())
r1 = Hooke_Jeeves(f, x0, tol, coef)
print("{:.10f} {:.10f}".format(r1[0], r1[1]))