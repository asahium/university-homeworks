"""
В коллекцию по одному добавляются целые числа. Первое добавляемое число равно A0, а все остальные вычисляются по правилу Ai = (Ai - 1 ⋅ X + Y) mod (109 + 7) (запись mod обозначает операцию взятия остатка от деления).
После добавления каждого числа определите, какое число является K-м по величине в коллекции. Если коллекция содержит меньше K элементов, ответом является число -1.

Формат ввода
Первая строка содержит целые числа N и K (1 ≤ N ≤ 105, 1 ≤ K ≤ N) — соответственно количество элементов массива и номер порядковой статистики.
Вторая строка содержит целые числа A0, X и Y (0 ≤ A0, X, Y ≤ 109) — соответственно начальный элемент массива и параметры для вычисления остальных элементов.

Формат вывода
Выведите одно целое число — сумму всех порядковых статистик.
"""



class MinHeap:
    def __init__(self, a, size):
        self.harr = a
        self.heap_size = size

    def buildHeap(self):
        i = int((self.heap_size - 1) / 2)
        while i >= 0:
            self.MinHeapify(i)
            i -= 1

    def parent(self, i):
        return int((i - 1) / 2)

    def left(self, i):
        return int(2 * i + 1)

    def right(self, i):
        return int(2 * i + 2)

    def extractMin(self):
        if (self.heap_size == 0):
            return 9999999999999
        root = self.harr[0]
        if self.heap_size > 1:
            self.harr[0] = self.harr[self.heap_size - 1]
            self.MinHeapify(0)
        heap_size -= 1
        return root

    def getMin(self):
        return self.harr[0]

    def replaceMin(self, x):
        self.harr[0] = x
        self.MinHeapify(0)

    def MinHeapify(self, i):
        l = self.left(i)
        r = self.right(i)
        smallest = i
        if l < self.heap_size and self.harr[l] < self.harr[i]:
            smallest = l
        if r < self.heap_size and self.harr[r] < self.harr[smallest]:
            smallest = r
        if smallest != i:
            self.harr[i], self.harr[smallest] = self.harr[smallest], self.harr[i]
            self.MinHeapify(smallest)


n, k = list(map(int, input().split()))
x, q, p = list(map(int, input().split()))
arr = []

# arr[0] = x
ans = 0
for i in range(n):
    #if i != 0:
     #   x = (x * p + q) % (10 ** 9 + 7)
    if i < k - 1:
        arr.append(x)
        ans -= 1
    if i == k - 1:
        arr.append(x)
        mh = MinHeap(arr, k)
        mh.buildHeap()
        ans += mh.getMin()
    if i > k - 1:
        if x > mh.getMin():
            mh.replaceMin(x)
        ans += mh.getMin()
    x = (x * q + p) % (10 ** 9 + 7)
print(ans)
