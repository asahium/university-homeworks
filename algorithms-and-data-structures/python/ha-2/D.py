"""
После долгих попыток устроиться на работу программистом, Макс наконец получил должность администратора в супермаркете. Заметив, что клиенты магазина часто подолгу ожидают своей очереди при оплате покупок, Макс решил создать автоматизированную систему, распределяющую покупателей по кассам.
В супермаркете имеются N касс, оператор i-й из которых пробивает одну покупку за время Ti. К кассам последовательно подходят M покупателей, у j-го из них в корзине находятся Aj покупок.
Каждого покупателя нужно направить к той кассе, которая начнёт его обслуживать раньше всех остальных. Если подходящих касс несколько, выбирается касса с наименьшим номером.
Напишите для Макса программу, которая подскажет каждому из покупателей, какую кассу ему следует выбрать.

Формат ввода
Первая строка содержит целое число N (1 ≤ N ≤ 105) — количество касс.
Вторая строка содержит N целых чисел Ti (1 ≤ Ti ≤ 105) — время, за которое операторы каждой из касс пробивают одну покупку.
Третья строка содержит целое число M (1 ≤ M ≤ 105) — количество покупателей.
Четвёртая строка содержит M целых чисел Ai (0 ≤ Ai ≤ 105) — количество покупок у каждого из покупателей.
Кассы нумеруются от 1 до N в порядке описания во входных данных.

Формат вывода
Выведите M целых чисел — номера касс, которые должны обслуживать каждого из покупателей. 
"""



import heapq

sellers_nums = int(input())
sellers_time = list(map(int, input().split()))
buyer_nums = int(input())
buyer_time = list(map(int, input().split()))
info = []
for i in range(sellers_nums):
    info.append([0, i + 1, sellers_time[i]])
bn = [(item[0], item) for item in info]
heapq.heapify(bn)
ans = []
for i in range(buyer_nums):
    a = heapq.heappop(bn)[1]
    ans.append(a[1])
    neww = [a[0] + a[2] * buyer_time[i], a[1], a[2]]
    heapq.heappush(bn, (neww[0], neww))
print(*ans)
