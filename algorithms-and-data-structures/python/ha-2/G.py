"""
Макс собрался пойти в кино, но перед ним встала проблема: в прокате очень много интересных фильмов, какой же из них следует выбрать?
Макс задумался, по каким критериям можно выбрать из фильмов лучший. Прежде всего, конечно, на выбор Макса влияет цена билета — чем она меньше, тем охотнее Макс пойдёт на фильм. Кроме этого, Макс на сайте любителей кино собрал положительные и отрицательные отзывы о каждом из фильмов. Чем больше у фильма положительных отзывов и чем меньше отрицательных, тем интереснее этот фильм для Макса.
Но как же объединить эти три характеристики? Ведь, например, фильм, о котором положительных отзывов больше всего, может быть далеко не самым дешёвым.
В итоге Макс решил поступить следующим образом. Он упорядочит список фильмов отдельно по каждой из характеристик и далее будет рассматривать только те фильмы, которые в каждом списке оказались среди 50% лучших (если общее количество фильмов нечётно, то Макс считает, что фильм, оказавшийся в середине рейтинга, также относится к 50% лучших).
Помогите Максу определить, сколько фильмов окажутся среди 50% лучших по каждой из характеристик.

Формат ввода
Первая строка содержит целое число N (1 ≤ N ≤ 105) — количество фильмов в прокате.
Следующие N строк описывают характеристики фильмов. Каждая из них содержит вещественное число Pi (1 ≤ Pi ≤ 5000). заданное с двумя знаками после десятичной точки, а также целые числа Ai и Bi (0 ≤ Ai, Bi ≤ 106) — соответственно цену билета на фильм, количество положительных отзывов о фильме и количество отрицательных отзывов о фильме. Ни у одной пары фильмов значения одной и той же характеристики не совпадают.

Формат вывода
Выведите одно целое число — количество фильмов, которые относятся к верхней половине рейтинга по каждой из трёх характеристик.
"""



import heapq

n = int(input())
info = []
ans = []

for i in range(n):
    info.append(list(map(float, input().split())))
    info[i].append(i)
    #    info[i][0] = -info[i][0]
    #    info[i][1] = -info[i][1]
    info[i][1] = -info[i][1]
list_by_first = []
list_by_second = []
list_by_third = []
list_by_first_final = []
list_by_second_final = []
list_by_third_final = []

if n % 2 == 0:
    polovina = int(n / 2)
else:
    polovina = int((n + 1) / 2)

list_by_first = [(item[0], item) for item in info]
heapq.heapify(list_by_first)
list_by_second = [(item[1], item) for item in info]
heapq.heapify(list_by_second)
list_by_third = [(item[2], item) for item in info]
heapq.heapify(list_by_third)

for i in range(polovina):
    a = heapq.heappop(list_by_first)[1]
    list_by_first_final.append(a[3])
    # heapq.heapify(list_by_first)

for i in range(polovina):
    a = heapq.heappop(list_by_second)[1]
    list_by_second_final.append(a[3])
    # heapq.heapify(list_by_second)

for i in range(polovina):
    a = heapq.heappop(list_by_third)[1]
    list_by_third_final.append(a[3])
    # heapq.heapify(list_by_third)

k = 0
a = list_by_first_final
b = list_by_second_final
c = list_by_third_final
#for i in list_by_first_final:
#    if i in list_by_second_final and i in list_by_third_final:
#        k += 1
#print(k)
print(len((set(a)).intersection((set(b)).intersection(set(c)))))
