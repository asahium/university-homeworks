# Проверяй что a,b,c равны нулю. Как бы бред, но все же.
# При таком варианте бесконечное количество решений.
# Также проверяй вариант когда a=0, тут получаем линейное уравнение bx+c = 0.
# но тут додумаешь.
# Я когда делал не думал, что в эту сторону надо копать, а оно вон как.
# Ну и вариант когда а и b раны нулю, а с нет.

a, b, c = float(input()), float(input()), float(input())

d = b ** 2 - 4 * a * c

if d >= 0 and a != 0:
    r = d ** 0.5
    x = [(-b - r) / (2 * a), (-b + r) / (2 * a)]
    x = sorted(set(x))

    print(*[len(x), *x])

elif a == 0:
    print(3)

elif d < 0:
    print(0)


# это не робит.