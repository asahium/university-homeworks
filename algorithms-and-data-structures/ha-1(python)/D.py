"""
Дан массив, элементами которого являются целые числа. Требуется вывести состояние этого массива после каждого шага сортировки слиянием.

Формат ввода
Первая строка содержит целое число N (2 ≤ N ≤ 104) — количество элементов массива.
Вторая строка содержит N целых чисел Ai (-231 ≤ Ai ≤ 231 - 1) — элементы массива.

Формат вывода
Выведите диапазоны массива в порядке завершения их обработки сортировкой слиянием (в конце каждого рекурсивного вызова сортировки выведите соответствующий отсортированный диапазон массива; см. примеры). 
"""



import math

def merge(A, B):
    Res = []
    i = 0
    j = 0
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            Res.append(A[i])
            i += 1
        else:
            Res.append(B[j])
            j += 1
    Res += A[i:] + B[j:]
    print(*Res)
    return Res


def merge_sort(s):
    if len(s) <= 1:
        print(*s)
        return s
    else:
        L = s[:math.ceil(len(s) / 2)]
        R = s[math.ceil(len(s) / 2):]
    return merge(merge_sort(L), merge_sort(R))


n = int(input())
s = list(map(int, input().split()))
s = merge_sort(s)
