"""
Дан массив, элементами которого являются целые числа. Требуется вывести состояние этого массива после заданного количества шагов сортировки выбором.

Формат ввода
Первая строка содержит целое число N (2 ≤ N ≤ 1000) — количество элементов массива.
Вторая строка содержит N целых чисел Ai (-231 ≤ Ai ≤ 231 - 1) — элементы массива.
Третья строка содержит целое число K (1 ≤ K ≤ N).

Формат вывода
Выведите N целых чисел — элементы массива в том порядке, в котором они находятся сразу после завершения K-й итерации внешнего цикла сортировки выбором (см. примеры). 
"""



def selection_sort(alist, k):
    global p
    for i in range(0, len(alist) - 1):
        smallest = i
        if i == k:
            print(*alist)
            p = True
        for j in range(i + 1, len(alist)):
            if alist[j] < alist[smallest]:
                smallest = j
        alist[i], alist[smallest] = alist[smallest], alist[i]


n = int(input())
old = list(map(int, input().split()))
k = int(input())
p = False
selection_sort(old, k)
if not p:
    print(*old)
