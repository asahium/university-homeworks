"""
Процедура heapify преобразует неупорядоченный массив в двоичную кучу, на вершине которой располагается максимальный элемент:
def heapify(arr):
    for i in range(len(arr) - 1, -1, -1):
        sift_down(arr, i)
Определите, сколько раз будет произведён обмен местами двух элементов массива при выполнении процедуры heapify.

Формат ввода
Первая строка содержит целое число N (1≤N≤104) — количество элементов массива.
Вторая строка содержит N целых чисел Ai (−231≤Ai<231) — элементы массива.

Формат вывода
Выведите одно целое число — количество обменов при вызове процедуры heapify для рассматриваемого массива. 
"""



class BinHeap:
    def __init__(self):
        self.heaplist = []
        self.heapsize = 0
        self.k = 0

    def left(self, i):
        return i * 2 + 1

    def right(self, i):
        return i * 2 + 2

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        if l <= self.heapsize and self.heaplist[l] > self.heaplist[i]:
            largest = l
        else:
            largest = i
        if r <= self.heapsize and self.heaplist[r] > self.heaplist[largest]:
            largest = r
        if largest != i:
            tmp = self.heaplist[i]
            self.heaplist[i] = self.heaplist[largest]
            self.heaplist[largest] = tmp
            self.heapify(largest)
            self.k += 1

    def buildHeap(self, list):
        self.heaplist = list
        self.heapsize = len(list) - 1
        for i in range(len(list) // 2, -1, -1):
            self.heapify(i)

    def heapSort(self):
        pass

    def extractMax(self):
        pass

    def getHeap(self):
        return self.k


n = int(input())
heap = BinHeap()
heap.buildHeap(list(map(int, input().split())))
print(heap.getHeap())
