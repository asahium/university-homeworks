"""
Дано натуральное число. Найдите число десятков в его десятичной записи (вторую справа цифру).

Формат ввода
Вводится единственное число.

Формат вывода
Выведите ответ на задачу.
"""



n = int(input())
print((n // 10) % 10)