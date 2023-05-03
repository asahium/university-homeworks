"""
Дан массив, элементами которого являются целые числа. Начальный элемент массива равен A0, а все остальные вычисляются по правилу Ai = (Ai - 1 ⋅ X + Y) mod (109 + 7) (запись mod обозначает операцию взятия остатка от деления).
Найдите минимальный элемент среди каждых M последовательных элементов массива (то есть от A0 до AM - 1, от A1 до AM, ..., от AN - M до AN - 1).

Формат ввода
Первая строка содержит целые числа N и M (1 ≤ N ≤ 105, 1 ≤ M ≤ N) — соответственно количество элементов массива и ширину скользящего окна.
Вторая строка содержит целые числа A0, X и Y (0 ≤ A0, X, Y ≤ 109) — соответственно начальный элемент массива и параметры для вычисления остальных элементов.

Формат вывода
Выведите одно целое число — сумму всех минимальных элементов.
"""



class StackWithMin:
    def __init__(self):
        self.Stack = []
        self.Min = []

    def top(self):
        return self.Stack[-1]

    def push(self, x):
        self.Stack.append(x)
        if (len(self.Stack) == 1):
            self.Min.append(x)
            return
        if (x < self.Min[-1]):
            self.Min.append(x)
        else:
            self.Min.append(self.Min[-1])

    def pop(self):
        self.Stack.pop()
        self.Min.pop()

    def isEmpty(self):
        if len(self.Stack) == 0:
            return True
        return False

    def getMin(self):
        return self.Min[-1]


class QueueWithMin:
    def __init__(self):
        self.s1 = StackWithMin()
        self.s2 = StackWithMin()

    def getMin(self):
        if (self.s1.isEmpty() or self.s2.isEmpty()):
            if self.s1.isEmpty():
                return self.s2.top()[1]
            else:
                return self.s1.top()[1]
        else:
            return min(self.s1.top()[1], self.s2.top()[1])

    def push(self, x):
        if self.s1.isEmpty():
            minimum = x
        else:
            minimum = min(x, self.s1.top()[1])
        self.s1.push([x, minimum])

    def pop(self):
        if (self.s2.isEmpty()):
            while not self.s1.isEmpty():
                element = self.s1.top()[0]
                self.s1.pop()
                if self.s2.isEmpty():
                    minimum = element
                else:
                    minimum = min(element, self.s2.top()[1])
                self.s2.push([element, minimum])
        self.s2.pop()


def nextEl(a, x, y):
    return (a * x + y) % (10 ** 9 + 7)


def slidingWindow(a, x, y, k, n):
    q = QueueWithMin()
    if k == n:
        for i in range(n):
            q.push(a)
            a = nextEl(a, x, y)
        return q.getMin()
    else:
        summa = 0
        for i in range(n):
            if i < k:
                q.push(a)
                a = nextEl(a, x, y)
                continue
            if i == k:
                summa += q.getMin()
            q.push(a)
            a = nextEl(a, x, y)
            q.pop()
            summa += q.getMin()
        return summa


n, m = list(map(int, input().split()))
a, x, y = list(map(int, input().split()))
print(slidingWindow(a, x, y, m, n))
