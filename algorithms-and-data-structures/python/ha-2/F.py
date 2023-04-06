"""
Рассмотрим следующую реализацию быстрой сортировки:

def quicksort(arr):

    ticks = len(arr)

    if len(arr) > 1:

        pivot = arr[len(arr) // 2]

        less = [elem for elem in arr if elem < pivot]

        greater = [elem for elem in arr if elem > pivot]

        ticks += quicksort(less)

        ticks += quicksort(greater)

        arr[:] = less + [pivot] + greater

    return ticks

Найдите такую перестановку чисел от 1 до N, при обработке которой показанная функция вернёт максимально возможное значение ticks.

Формат ввода
Ввод содержит целое число N (1≤N≤104).

Формат вывода
Выведите любую перестановку целых чисел от 1 до N, после обработки которой значение ticks будет максимально возможным. 
"""



n = int(input())
if n % 2 == 1:
    for i in range((n + 1) // 2, 0, -1):
        print(2 * i - 1, end=" ")
    for i in range(1, (n - 1) // 2 + 1):
        print(i * 2, end=" ")
else:
    for i in range(n // 2, 0, -1):
        print(2 * i, end=" ")
    for i in range(n // 2):
        print(2 * i + 1, end=" ")
