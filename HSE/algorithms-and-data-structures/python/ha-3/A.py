"""
ан массив, элементами которого являются целые числа. Начальный элемент массива равен A0, а все остальные вычисляются по правилу Ai = (Ai - 1 ⋅ X + Y) mod 11 (запись mod обозначает операцию взятия остатка от деления).
Требуется отсортировать этот массив по неубыванию.

Формат ввода
Первая строка содержит целое число N (1 ≤ N ≤ 107) — количество элементов массива.
Вторая строка содержит целые числа A0, X и Y (0 ≤ A0, X, Y ≤ 10) — соответственно начальный элемент массива и параметры для вычисления остальных элементов.

Формат вывода
Выведите одно целое число — сумму после сортировки массива. 
"""



am = [0] * 11
ans = 0
n = int(input())
a, x, y = list(map(int, input().split()))
for i in range(n):
    am[a] += 1
    a = (a * x + y) % 11
a0_final = 0 * am[0]
a1_final = 1 * (2 * am[0] + am[1] - 1) * am[1] / 2
a2_final = 2 * (2 * (am[0] + am[1]) + am[2] - 1) * am[2] / 2
a3_final = 3 * (2 * (am[0] + am[1] + am[2]) + am[3] - 1) * am[3] / 2
a4_final = 4 * (2 * (am[0] + am[1] + am[2] + am[3]) + am[4] - 1) * am[4] / 2
a5_nonfinal = (am[0] + am[1] + am[2] + am[3] + am[4])
a5_final = 5 * (2 * a5_nonfinal + am[5] - 1) * am[5] / 2
a6_nonfinal = (am[0] + am[1] + am[2] + am[3] + am[4] + am[5])
a6_final = 6 * (2 * a6_nonfinal + am[6] - 1) * am[6] / 2
a7_nonfinal = am[0] + am[1] + am[2] + am[3] + am[4] + am[5] + am[6]
a7_final = 7 * (2 * a7_nonfinal + am[7] - 1) * am[7] / 2
a8_nonfinal = am[0] + am[1] + am[2] + am[3] + am[4] + am[5] + am[6] + am[7]
a8_final = 8 * (2 * a8_nonfinal + am[8] - 1) * am[8] / 2
a9_nonfinal = am[0] + am[1] + am[2] + am[3] + am[4] + \
              am[5] + am[6] + am[7] + am[8]
a9_final = 9 * (2 * a9_nonfinal + am[9] - 1) * am[9] / 2
a10_nonfinal = am[0] + am[1] + am[2] + am[3] + am[4] + \
               am[5] + am[6] + am[7] + am[8] + am[9]
a10_final = 10 * (2 * a10_nonfinal + am[10] - 1) * \
            am[10] / 2
ans = a0_final + a1_final + a2_final + a3_final + a4_final + \
      a5_final + a6_final + a7_final + a8_final + \
      +a9_final + a10_final
print(int(ans))
