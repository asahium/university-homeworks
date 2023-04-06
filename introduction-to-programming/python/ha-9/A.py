"""
Реализуйте класс Matrix. Он должен содержать:
    Конструктор от списка списков. Гарантируется, что списки состоят из чисел, не пусты и все имеют одинаковый размер. Конструктор должен копировать содержимое списка списков, т.е. при изменении списков, от которых была сконструирована матрица, содержимое матрицы изменяться не должно.
    Метод __str__ переводящий матрицу в строку. При этом элементы внутри одной строки должны быть разделены знаками табуляции, а строки — переносами строк. При этом после каждой строки не должно быть символа табуляции и в конце не должно быть переноса строки.
    Метод size без аргументов, возвращающий кортеж вида (число строк, число столбцов)

На проверку вы должны сдать только файл, содержащий описание класса и одну строку вне класса (в качестве основной программы):
exec(stdin.read())
И в начале файла:
from sys import stdin
Для тестирования класса вы можете вместо строки exec(stdin.read()) вставлять код из примеров или писать свой код.

Формат ввода
Вводится исходный код тестирующей программы на языке Python.

Формат вывода
Выведите результат её работы в текущем окружении при помощи exec как это указано в условии.
"""



from sys import stdin
from copy import deepcopy


class Matrix:
    def __init__(self, list):
        self.list = deepcopy(list)

    def __str__(self):
        rows = []
        for row in self.list:
            rows.append('\t'.join(map(str, row)))
        return '\n'.join(rows)

    def size(self):
        return len(self.list), len(self.list[0])


exec(stdin.read())