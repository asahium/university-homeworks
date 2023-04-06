"""
Дано число N. С начала суток прошло N минут. Определите, сколько часов и минут будут показывать электронные часы в этот момент.

Формат ввода
Вводится число N — целое, положительное, не превышает 107.

Формат вывода
Программа должна вывести два числа: количество часов (от 0 до 23) и количество минут (от 0 до 59).
Учтите, что число N может быть больше, чем количество минут в сутках.

"""



n = int(input())
h = n % (60 * 24) // 60
m = n % 60
print(h, m)