"""
Мише и Маше нужно срочно напечатать N листов с условиями замечательной задачи.
Принтер Миши печатает один лист за X секунд, принтер Маши — за Y секунд. За какое минимальное время они оба сумеют отпечатать N листов?

Формат ввода
Ввод содержит целые числа N, X и Y (1 ≤ N ≤ 2 ⋅ 108, 1 ≤ X, Y ≤ 10).

Формат вывода
Выведите одно целое число — минимальное время в секундах, необходимое для получения N копий.
"""



def f(a1, n1, x1, y1):
    return max(a1 * x1, (n1 - a1) * y1)


n, x, y = list(map(int, input().split()))
if x == y:
    print(min(f(n // 2, n, x, y), f(n // 2 + 1, n, x, y)))
else:
    left = 0
    r = n
    while r - left > 3:
        m1 = left + (r - left) // 3
        m2 = r - (r - left) // 3
        if f(m1, n, x, y) < f(m2, n, x, y):
            r = m2
        else:
            left = m1
    if r - left == 0:
        print(f(left, n, x, y))
    elif r - left == 1:
        print(min(f(left, n, x, y), f(left + 1, n, x, y), f(r, n, x, y)))
    else:
        print(min(f(left, n, x, y), f(left + 1, n, x, y),
                  f(left + 2, n, x, y), f(r, n, x, y)))
