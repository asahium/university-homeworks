"""
Реализуйте приоритетную очередь на двоичной куче, элементами которой являются целые числа. В корне кучи должен располагаться максимальный элемент.
Вы должны поддерживать следующие виды операций:
    push X — добавить в очередь элемент X;
    pop — вывести максимальный элемент и извлечь его;
    get I — вывести элемент, располагающийся в куче по индексу I, не извлекая его.
Значения X принадлежат диапазону [-109; 109]. Вызов операций pop происходит только тогда, когда очередь не пуста. Значения I принадлежат диапазону [0, L), где L — текущий размер очереди.

Формат ввода
Первая строка содержит целое число N (1 ≤ N ≤ 105) — количество операций.
Следующие N строк описывают операции.

Формат вывода
Для каждой операции pop и get выведите на отдельной строке одно целое число — соответствующий элемент. 
"""



import heapq


class MaxHeapObj(object):
    def __init__(self, val): self.val = val

    def __lt__(self, other): return self.val > other.val

    def __eq__(self, other): return self.val == other.val

    def __str__(self): return str(self.val)


class QueueOnHeap(object):
    def __init__(self):
        self.h = []

    def heappush(self, x):
        heapq.heappush(self.h, x)

    def heappop(self):
        return heapq.heappop(self.h)

    def getitem(self, i):
        return self.h[i].val

    def heappush(self, x):
        heapq.heappush(self.h, MaxHeapObj(x))

    def heappop(self):
        return heapq.heappop(self.h).val


priorityqueue = QueueOnHeap()
n = int(input())
for i in range(n):
    imp = input()
    if imp[:2] == 'pu':
        priorityqueue.heappush(int(imp[5:]))
    if imp == 'pop':
        print(priorityqueue.heappop())
    if imp[:2] == 'ge':
        print(priorityqueue.getitem(int(imp[4:])))
